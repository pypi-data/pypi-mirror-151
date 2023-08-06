import { INflxAnalytics } from '@netflix-internal/jupyterlab-analytics';
import { JupyterFrontEnd } from '@jupyterlab/application';
import { Widget } from '@lumino/widgets';
import { FeedbackWidget } from './slackfeedback';

export const openTimelineCommand = 'timeline:open';
export const cloneVersionCommand = 'timeline:clone';
export const restoreVersionCommand = 'timeline:restore';
export const openTimelineVersionCommand = 'timeline:open-version';
export const openSlackFeedbackCommand = 'slack-feedback:open';
export function addCommands(app: JupyterFrontEnd, nfa: INflxAnalytics): void {
  app.commands.addCommand(openSlackFeedbackCommand, {
    label: 'Open Slack Feedback Modal',
    caption: 'Open Slack Feedback Modal',
    execute: () => {
      const widget = new FeedbackWidget(nfa);
      nfa.logFeatureEngaged('timeline', 'sidebar-opened');
      if (!document.getElementById('feedback-slack'))
        Widget.attach(widget, document.body);
    }
  });
}
