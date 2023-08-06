import * as React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
import {
  ITranslator,
  nullTranslator,
  TranslationBundle
} from '@jupyterlab/translation';

interface IToolbarProps {
  trans: TranslationBundle;
  handlers: IActionHandlers;
}

const ContentHeaderToolbar = (props: IToolbarProps) => {
  const { trans, handlers } = props;

  return (
    <div>
      {trans.__('Do you wish to ')}
      <span onClick={handlers.onAcceptChanges}>
        {trans.__('Accept')}
      </span> or{' '}
      <span onClick={handlers.onDeclineChanges}>{trans.__('Decline')}</span>
      {trans.__(' these changes?')}
    </div>
  );
};

interface IActionHandlers {
  onAcceptChanges: () => void;
  onDeclineChanges: () => void;
}

export class ContentHeaderWidget extends ReactWidget {
  constructor(handlers: IActionHandlers, translator?: ITranslator) {
    super();
    this._trans = (translator || nullTranslator).load('jupyterlab');
    this._handlers = handlers;
    this.addClass('mutable-ai-content-header');
  }

  render(): JSX.Element {
    return (
      <ContentHeaderToolbar trans={this._trans} handlers={this._handlers} />
    );
  }

  private _trans: TranslationBundle;
  private _handlers: IActionHandlers;
}
