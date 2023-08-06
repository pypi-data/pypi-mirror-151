/* eslint-disable @typescript-eslint/ban-ts-comment */
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

// Modified from jupyterlab/packages/completer/src/contextconnector.ts
import { Cell } from '@jupyterlab/cells';

import { CodeEditor } from '@jupyterlab/codeeditor';
import { DataConnector } from '@jupyterlab/statedb';
import { CompletionHandler } from '@jupyterlab/completer';
import { requestAPI } from '../handler';
import { NotebookPanel } from '@jupyterlab/notebook';
import { ISettingRegistry } from '@jupyterlab/settingregistry';

/**
 * A custom connector for completion handlers.
 */
export class CustomConnector extends DataConnector<
  CompletionHandler.IReply,
  void,
  CompletionHandler.IRequest
> {
  private _panel: NotebookPanel;
  private setting: ISettingRegistry.ISettings;
  /**
   * Create a new custom connector for completion requests.
   *
   * @param options - The instatiation options for the custom connector.
   */
  constructor(
    options: CustomConnector.IOptions,
    panel: NotebookPanel,
    setting: ISettingRegistry.ISettings
  ) {
    super();
    // @ts-ignore
    this._editor = options.editor;
    this._panel = panel;
    this.setting = setting;
  }

  /**
   * Fetch completion requests.
   *
   * @param request - The completion request text and details.
   * @returns Completion reply
   */
  fetch(
    request: CompletionHandler.IRequest
  ): Promise<CompletionHandler.IReply> {
    if (!this._editor) {
      return Promise.reject('No editor');
    }
    return new Promise<CompletionHandler.IReply>(resolve => {
      const apiKey = this.setting.get('apiKey').composite as string;
      const flag = this.setting.get('flag').composite as boolean;
      const enabled = this.setting.get('enabled').composite as boolean;
      const autocompleteDomain = this.setting.get('autocompleteDomain')
        .composite as string;

      resolve(
        Private.completionHint(
          // @ts-ignore
          this._editor,
          this._panel,
          autocompleteDomain,
          apiKey,
          flag && enabled
        )
      );
    });
  }

  private _editor: CodeEditor.IEditor | null;
}

interface ITextData {
  prompt: string;
  suffix: string;
}

function processCellStringData(
  cells: ReadonlyArray<Cell>,
  index: number,
  cursor: CodeEditor.IPosition
): ITextData {
  // get all cells up to index
  const cellsUpToIndex = cells.slice(0, index);

  // get all cells after index
  const cellsAfterIndex = cells.slice(index + 1, cells.length);

  const cellTextBefore = cellsUpToIndex
    .map(cell => cell.model.value.text)
    .join('\n');

  const cellTextCurrent = cells[index].model.value.text;

  const cellTextAfter = cellsAfterIndex
    .map(cell => cell.model.value.text)
    .join('\n');

  let beforeText: string = cellTextBefore;
  const afterTextSplit = cellTextCurrent.split('\n');
  beforeText += '\n\n' + afterTextSplit.splice(0, cursor.line).join('\n');
  const cursorText = afterTextSplit.splice(0, 1)[0];
  beforeText += '\n' + cursorText.slice(0, cursor.column);
  const afterText: string =
    cursorText.slice(cursor.column, cursorText.length) +
    '\n' +
    afterTextSplit.join('\n') +
    cellTextAfter;

  return {
    prompt: beforeText,
    suffix: afterText
  };
}

/**
 * A namespace for custom connector statics.
 */
export namespace CustomConnector {
  /**
   * The instantiation options for cell completion handlers.
   */
  export interface IOptions {
    /**
     * The session used by the custom connector.
     */
    editor: CodeEditor.IEditor | null;
  }
}

/**
 * A namespace for Private functionality.
 */
namespace Private {
  /**
   * Get a list of mocked completion hints.
   *
   * @param editor Editor
   * @returns Completion reply
   */
  export async function completionHint(
    editor: CodeEditor.IEditor,
    panel: NotebookPanel,
    domain: string,
    apiKey: string,
    flag: boolean
  ): Promise<CompletionHandler.IReply> {
    // Find the token at the cursor
    const cursor = editor.getCursorPosition();
    const token = editor.getTokenForPosition(cursor);

    // get source of all cells
    const cells = panel.content.widgets;

    // get index of active cell
    // @ts-ignore
    const index = cells.indexOf(panel.content.activeCell);

    const data = processCellStringData(cells, index, cursor);

    // Get all text in the editor
    //const activeCellText = editor.model.value.text;

    // get token string
    const tokenString = token.value;

    // Send to handler
    // TODO: rename this line to prompt
    const dataToSend = { data, domain, apiKey, flag };

    // POST request
    let reply = requestAPI<any>('AUTOCOMPLETE', {
      body: JSON.stringify(dataToSend),
      method: 'POST'
    });

    const response = await reply;

    // Get size of text so that you can remove it from response
    //const size = previousText.length;
    //console.log("size of text: " + size);
    // Remove initial text in response
    // const responseText = response.slice(size);
    console.log('response: ' + response);

    // Create a list of matching tokens.
    const tokenList = [
      { value: tokenString + response, offset: token.offset, type: 'AI' }
      //{ value: token.value + 'Magic', offset: token.offset, type: 'magic' },
      //{ value: token.value + 'Neither', offset: token.offset },
    ];

    //console.log("value and offset")
    //console.log(token.value)
    //console.log(token.offset)
    // Only choose the ones that have a non-empty type field, which are likely to be of interest.
    const completionList = tokenList.filter(t => t.type).map(t => t.value);
    // Remove duplicate completions from the list
    const matches = Array.from(new Set<string>(completionList));

    return {
      start: token.offset,
      end: token.offset + token.value.length,
      matches,
      metadata: {}
    };
  }
}
