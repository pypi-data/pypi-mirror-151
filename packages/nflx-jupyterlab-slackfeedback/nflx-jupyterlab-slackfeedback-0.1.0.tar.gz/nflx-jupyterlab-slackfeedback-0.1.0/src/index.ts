import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { SlackFeedbackButtonExtension } from './buttons';
import { addCommands } from './commands';
import { INflxAnalytics } from '@netflix-internal/jupyterlab-analytics';

/**
 * Initialization data for the nflx-jupyterlab-slackfeedback extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'nflx-jupyterlab-slackfeedback:plugin',
  autoStart: true,
  requires: [INflxAnalytics],
  activate: activate
};

async function activate(
  app: JupyterFrontEnd,
  analytics: INflxAnalytics
): Promise<void> {
  console.log(
    'JupyterLab extension nflx-jupyterlab-slackfeedback is activated!'
  );

  app.docRegistry.addWidgetExtension(
    'notebook',
    new SlackFeedbackButtonExtension(app.commands, analytics)
  );
  addCommands(app, analytics);
}

export default plugin;
