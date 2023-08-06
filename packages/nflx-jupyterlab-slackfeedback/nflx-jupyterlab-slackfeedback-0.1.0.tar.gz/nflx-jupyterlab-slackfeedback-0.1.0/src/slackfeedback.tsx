import React, { useEffect } from 'react';
import SlackFeedback, { themes } from 'react-slack-feedback';
import { ReactWidget } from '@jupyterlab/apputils';
import { style } from 'typestyle';
import { Typography } from '@material-ui/core';
import ReactDOM from 'react-dom';
import { INflxAnalytics } from '@netflix-internal/jupyterlab-analytics';

const panelWrapperClass = style({
  display: 'flex',
  flexDirection: 'column',
  height: '100%',
  overflowY: 'auto',
  backgroundColor: 'var(--jp-layout-color1)!important'
});
function sendToServer(payload: any, success: any, error: any, nfa: any) {
  switch (payload.attachments[0].title) {
    case 'bug':
      nfa.logFeatureEngaged('jl-user-feedback', 'bug');
      break;
    case 'feature':
      nfa.logFeatureEngaged('jl-user-feedback', 'feauture');
      break;
    case 'improvement':
      nfa.logFeatureEngaged('jl-user-feedback', 'improvement');
      break;
  }

  payload['attachments'][0].author_name =
    window.location.pathname.split('/')[1] + '@netflix.com';
  return fetch(`${getJupyterPrefix()}api/slack/messages`, {
    method: 'POST',
    body: JSON.stringify(payload),
    mode: 'no-cors'
  })
    .then(success => removeElement())
    .catch(error);
}

export class FeedbackWidget extends ReactWidget {
  nfa: INflxAnalytics;
  constructor(props: INflxAnalytics) {
    super();
    this.addClass(panelWrapperClass);
    this.nfa = props;
  }

  render(): JSX.Element {
    return <SlackFeedbackComponent analytics={this.nfa} />;
  }
}

const removeElement = () => {
  let slackFeedbackElement = document.getElementById('feedback-slack');
  slackFeedbackElement?.remove();
};

function SlackFeedbackComponent(props: { analytics: any }) {
  let slackFeedback = document.getElementById('channel!');

  const officeHoursInfo = () => {
    return (
      <div style={{ marginBottom: '16px' }}>
        <Typography style={{ fontSize: '16px', color: '#0088ff' }}>
          Notebooks team has office hours!
        </Typography>
        <Typography style={{ fontSize: '14px', color: 'GrayText' }}>
          Join us every Thursday from 1-2pm PST
        </Typography>

        <a
          color="textSecondary"
          style={{ fontSize: '14px', color: 'HighlightText' }}
          href="https://docs.google.com/spreadsheets/d/16ZybsUjazQltdTS1KPE8vob1imZ6E30kv-DUQFqjzsc/edit#gid=0"
          target="_blank"
          rel="noopener noreferrer"
        >
          Sign up here
        </a>
      </div>
    );
  };
  useEffect(() => {
    if (document.getElementById('channel'))
      ReactDOM.render(officeHoursInfo(), document.getElementById('channel'));
  }, [slackFeedback]);

  return (
    <div id="feedback-slack">
      <SlackFeedback
        style={{ display: 'none' }}
        open={true}
        channel="#ask-notebooks"
        theme={themes.default}
        onClose={() => removeElement()}
        onSubmit={(payload: any, success: any, error: any) =>
          sendToServer(payload, success, error, props.analytics)
            .then(success)
            .catch(error)
        }
      />
    </div>
  );
}
export function getJupyterPrefix(): string {
  const windowPath = window.location.pathname;
  return windowPath.substring(0, windowPath.indexOf('lab'));
}
