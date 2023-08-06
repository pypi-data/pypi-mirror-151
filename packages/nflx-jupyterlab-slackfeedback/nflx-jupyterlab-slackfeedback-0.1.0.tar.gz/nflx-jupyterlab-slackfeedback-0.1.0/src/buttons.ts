import { ToolbarButton } from '@jupyterlab/apputils';
import { DocumentRegistry } from '@jupyterlab/docregistry';
import { INotebookModel, NotebookPanel } from '@jupyterlab/notebook';
import { CommandRegistry } from '@lumino/commands';
import { DisposableDelegate, IDisposable } from '@lumino/disposable';
import { openSlackFeedbackCommand } from './commands';
import { slackIcon } from './icons';
import { INflxAnalytics } from '@netflix-internal/jupyterlab-analytics';

export class SlackFeedbackButtonExtension
  implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel>
{
  private readonly commands: CommandRegistry;
  private readonly nfa: INflxAnalytics;

  constructor(commands: CommandRegistry, _nfa: INflxAnalytics) {
    this.commands = commands;
    this.nfa = _nfa;
  }

  createNew(
    widget: NotebookPanel,
    _context: DocumentRegistry.IContext<INotebookModel>
  ): void | IDisposable {
    const button = new ToolbarButton({
      label: 'Send Feedback',
      tooltip: 'Send feedback to the Notebooks team slack channel',
      icon: slackIcon,
      onClick: () => {
        this.commands.execute(openSlackFeedbackCommand);
        this.nfa.logFeatureEngaged('jl-user-feedback', 'toolbar-button-click');
      }
    });

    widget.toolbar.insertAfter('spacer', 'slack-feedback', button);
    return new DisposableDelegate(() => {
      button.dispose();
    });
  }
}
