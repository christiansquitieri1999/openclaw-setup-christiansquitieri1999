import { readFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';

function requireCondition(condition, message) {
  if (!condition) throw new Error(message);
}

function localTimestamp(date, formatter) {
  const parts = Object.fromEntries(
    formatter.formatToParts(date).map(({ type, value }) => [type, value]),
  );
  return `${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}:${parts.second}`;
}

export function checkPlan(plan) {
  requireCondition(plan && typeof plan === 'object', 'A plan object is required.');
  requireCondition(typeof plan.title === 'string' && plan.title.trim(), 'Title is required.');
  requireCondition(typeof plan.timezone === 'string', 'Timezone is required.');
  const formatter = new Intl.DateTimeFormat('en-GB', {
    timeZone: plan.timezone,
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit', hourCycle: 'h23',
  });
  for (const field of ['startDate', 'endDate']) {
    const value = plan[field];
    requireCondition(typeof value === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(value), `${field} must be YYYY-MM-DD.`);
    const date = new Date(`${value}T00:00:00Z`);
    requireCondition(Number.isFinite(date.getTime()) && date.toISOString().slice(0, 10) === value, `${field} is invalid.`);
  }
  requireCondition(plan.startDate <= plan.endDate, 'Planning window is reversed.');
  requireCondition(Array.isArray(plan.projects) && plan.projects.length > 0, 'Projects are required.');
  requireCondition(Array.isArray(plan.sessions) && plan.sessions.length > 0, 'Sessions are required.');
  const minutes = new Map();
  for (const project of plan.projects) {
    requireCondition(project && typeof project.name === 'string' && project.name.trim(), 'Project name is required.');
    requireCondition(!minutes.has(project.name), `Duplicate project: ${project.name}`);
    requireCondition(Number.isFinite(project.hours) && project.hours > 0 && Number.isInteger(project.hours * 60), `Invalid effort: ${project.name}`);
    minutes.set(project.name, 0);
  }
  let previousEnd = -Infinity;
  let previousProject = -1;
  const sessions = plan.sessions.map((session) => {
    requireCondition(session && minutes.has(session.project), 'Session references an unknown project.');
    const dates = ['start', 'end'].map((field) => {
      const value = session[field];
      requireCondition(typeof value === 'string' && /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}$/.test(value), `${field} requires an offset-aware timestamp.`);
      const date = new Date(value);
      requireCondition(Number.isFinite(date.getTime()), `Invalid ${field} timestamp.`);
      const local = localTimestamp(date, formatter);
      requireCondition(local === value.slice(0, 19), `${field} does not match timezone ${plan.timezone}.`);
      const day = local.slice(0, 10);
      requireCondition(day >= plan.startDate && day <= plan.endDate, 'Session is outside the agreed window.');
      return date.getTime();
    });
    const durationMinutes = (dates[1] - dates[0]) / 60000;
    requireCondition(durationMinutes > 0 && Number.isInteger(durationMinutes), 'Session duration must be positive whole minutes.');
    requireCondition(dates[0] >= previousEnd, 'Sessions overlap or are not chronological.');
    const projectIndex = plan.projects.findIndex(({ name }) => name === session.project);
    requireCondition(projectIndex >= previousProject, 'Session violates the agreed project order.');
    previousProject = projectIndex;
    previousEnd = dates[1];
    minutes.set(session.project, minutes.get(session.project) + durationMinutes);
    return { project: session.project, start: session.start, end: session.end, durationMinutes };
  });
  for (const project of plan.projects) {
    requireCondition(minutes.get(project.name) === project.hours * 60, `Effort mismatch for ${project.name}.`);
  }
  return {
    title: plan.title,
    timezone: plan.timezone,
    startDate: plan.startDate,
    endDate: plan.endDate,
    totalHours: [...minutes.values()].reduce((sum, value) => sum + value, 0) / 60,
    projects: plan.projects.map(({ name, hours }) => ({ name, hours })),
    sessions,
  };
}

export function checkCalendarEvent(event, expected) {
  requireCondition(event && typeof event === 'object', 'An event object is required.');
  requireCondition(event.id === expected.id && event.status === 'confirmed', 'Event ID or status mismatch.');
  requireCondition(event.summary === expected.summary, 'Event title mismatch.');
  requireCondition(Date.parse(event.start?.dateTime) === Date.parse(expected.session.start), 'Event start mismatch.');
  requireCondition(Date.parse(event.end?.dateTime) === Date.parse(expected.session.end), 'Event end mismatch.');
  requireCondition(event.visibility === 'private', 'Event must be private.');
  // Google Calendar defines omitted transparency as opaque (busy).
  requireCondition((event.transparency ?? 'opaque') === 'opaque', 'Event must block time.');
  requireCondition(event.reminders?.useDefault === false && !event.reminders.overrides?.length, 'Event must have no reminders.');
  requireCondition(!event.attendees?.length && !event.attendeesOmitted, 'Unexpected or omitted attendees.');
  requireCondition(!event.recurrence?.length && !event.recurringEventId, 'Event must be a single session.');
  requireCondition(!event.conferenceData && !event.hangoutLink, 'Event must have no conference.');
  requireCondition(event.description === expected.description, 'Event description mismatch.');
  requireCondition(event.organizer?.email === expected.calendarId, 'Event calendar mismatch.');
  requireCondition(typeof event.htmlLink === 'string' && event.htmlLink.startsWith('https://'), 'Event link is missing.');
  return {
    id: event.id, htmlLink: event.htmlLink, start: event.start, end: event.end,
    durationMinutes: (Date.parse(event.end.dateTime) - Date.parse(event.start.dateTime)) / 60000,
    visibility: event.visibility, transparency: event.transparency ?? 'opaque',
    reminders: event.reminders,
  };
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    requireCondition(process.argv.length === 3, 'Usage: node check-plan.mjs <plan.json>');
    console.log(JSON.stringify(checkPlan(JSON.parse(readFileSync(process.argv[2], 'utf8'))), null, 2));
  } catch (error) {
    console.error(`Plan validation failed: ${error.message}`);
    process.exitCode = 1;
  }
}
