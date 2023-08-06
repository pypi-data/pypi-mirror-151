import { JupyterFrontEnd } from '@jupyterlab/application';
import { DocumentRegistry, IDocumentWidget } from '@jupyterlab/docregistry';
import { MainAreaWidget } from '@jupyterlab/apputils';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { ContentHeaderWidget } from './widgets/ContentHeaderToolbar';
import { requestAPI } from './handler';

interface ITransformPollingManagerProps {
  docManager: IDocumentManager;
  app: JupyterFrontEnd;
}

interface IPolling {
  id: string;
  filename: string;
  dirname: string;
  status: boolean;
  count: number;
}

interface ICheckStatusResponse {
  status: string;
  file: string;
}

interface IFileChangeResponse {
  status: string;
}

export class TransformPollingManager {
  constructor(props: ITransformPollingManagerProps) {
    this._docManager = props.docManager;
    this._app = props.app;

    this.polling = {
      id: '',
      filename: '',
      dirname: '',
      status: false,
      count: 0
    };

    this.pollingCache = {
      id: '',
      filename: '',
      dirname: '',
      status: false,
      count: 0
    };

    this.startPolling = this.startPolling.bind(this);
    this.openTransformedFile = this.openTransformedFile.bind(this);

    this.acceptFile = this.acceptFile.bind(this);
    this.declineFile = this.declineFile.bind(this);
  }

  startPolling(uid: string, filename: string, dirname: string): void {
    if (this.polling.status) {
      return;
    }
    this.polling = {
      id: uid,
      filename: filename,
      dirname: dirname,
      status: true,
      count: 0
    };

    const dataToSend = { uid, dirname };

    const pollingRef = setInterval(() => {
      const reply = requestAPI<any>('CHECK_STATUS', {
        body: JSON.stringify(dataToSend),
        method: 'POST'
      });

      this.polling = {
        ...this.polling,
        count: this.polling.count + 1
      };

      reply
        .then((response: ICheckStatusResponse) => {
          if (response.status === 'finished') {
            this.pollingCache = {
              ...this.polling
            };
            this.polling = {
              id: '',
              filename: '',
              dirname: '',
              status: false,
              count: 0
            };
            clearInterval(pollingRef);
            this.openTransformedFile(response.file);
          } else {
            if (this.polling.count >= 60) {
              this.pollingCache = {
                id: '',
                filename: '',
                dirname: '',
                status: false,
                count: 0
              };
              this.polling = {
                id: '',
                filename: '',
                dirname: '',
                status: false,
                count: 0
              };
              clearInterval(pollingRef);
            }
          }
        })
        .catch(e => console.log('Transformation failed!', e));
    }, 1000);
  }

  acceptFile() {
    const dataToSend = {
      uid: this.pollingCache.id,
      filename: this.pollingCache.filename,
      dirname: this.pollingCache.dirname
    };

    const reply = requestAPI<any>('ACCEPT_FILE', {
      body: JSON.stringify(dataToSend),
      method: 'POST'
    });
    this.pollingCache = {
      id: '',
      filename: '',
      dirname: '',
      status: false,
      count: 0
    };
    reply
      .then((response: IFileChangeResponse) => {
        if (response.status === 'completed') {
          console.log('File accepted.');
          const path = this._oldFile?.context.path;

          if (this._oldFile) {
            this._oldFile.close();
          }

          if (this._newFile) {
            this._newFile.close();
          }

          if (path) {
            setTimeout(() => {
              this._docManager.open(path);
              const launcher = this._app.shell.widgets('main').next();
              if (launcher?.title.label === 'Launcher') {
                setTimeout(() => {
                  launcher.close();
                }, 300);
              }
            }, 300);
          }
        } else {
          console.log('File accepting failed.');
        }
      })
      .catch(e => console.log('File accepting failed.', e));
  }

  declineFile() {
    const dataToSend = {
      uid: this.pollingCache.id,
      dirname: this.pollingCache.dirname
    };

    const reply = requestAPI<any>('DECLINE_FILE', {
      body: JSON.stringify(dataToSend),
      method: 'POST'
    });
    this.pollingCache = {
      id: '',
      filename: '',
      dirname: '',
      status: false,
      count: 0
    };
    reply
      .then((response: IFileChangeResponse) => {
        if (response.status === 'completed') {
          console.log('File decline.');
          const path = this._oldFile?.context.path;

          if (this._oldFile) {
            this._oldFile.close();
          }

          if (this._newFile) {
            this._newFile.close();
          }

          if (path) {
            setTimeout(() => {
              this._docManager.open(path);
              const launcher = this._app.shell.widgets('main').next();
              if (launcher?.title.label === 'Launcher') {
                setTimeout(() => {
                  launcher.close();
                }, 300);
              }
            }, 100);
          }
        } else {
          console.log('File declining failed.');
        }
      })
      .catch(e => console.log('File declining failed.', e));
  }

  openTransformedFile(transformedPath: string) {
    const options: DocumentRegistry.IOpenOptions = {
      mode: 'split-right'
    };

    const oldPath =
      this.pollingCache.dirname + '/' + this.pollingCache.filename;
    const newPath =
      this.pollingCache.dirname +
      '/.' +
      this.pollingCache.id +
      '/mutableai_transform/' +
      this.pollingCache.filename;

    this._docManager.closeFile(oldPath);

    setTimeout(() => {
      this._oldFile = this._docManager.open(oldPath);
      this._newFile = this._docManager.open(
        newPath,
        undefined,
        undefined,
        options
      );

      if (this._newFile instanceof MainAreaWidget) {
        // Create a widget
        const widgetC = new ContentHeaderWidget({
          onAcceptChanges: this.acceptFile,
          onDeclineChanges: this.declineFile
        });

        // and insert it into the header
        this._newFile.contentHeader.addWidget(widgetC);
        const launcher = this._app.shell.widgets('main').next();

        if (launcher?.title.label === 'Launcher') {
          setTimeout(() => {
            launcher.close();
          }, 300);
        }
      }
    }, 300);
  }

  private _oldFile: IDocumentWidget | undefined;
  private _newFile: IDocumentWidget | undefined;
  private _docManager: IDocumentManager;
  private _app: JupyterFrontEnd;

  private polling: IPolling;
  private pollingCache: IPolling;
}
