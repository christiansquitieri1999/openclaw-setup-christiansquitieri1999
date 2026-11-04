import assert from 'node:assert/strict';
import test from 'node:test';
import { checkCalendarEvent, checkPlan } from './check-plan.mjs';

function realPlan() {
  return {
    title: 'Piano operativo',
    timezone: 'Europe/Rome',
    startDate: '2026-11-24',
    endDate: '2026-12-10',
    projects: [
      { name: 'Backend', hours: 4 },
      { name: 'Database', hours: 4 },
      { name: 'RAG', hours: 4 },
    ],
    sessions: [
      ['Backend', '2026-11-24'],
      ['Backend', '2026-11-26'],
      ['Database', '2026-12-01'],
      ['Database', '2026-12-03'],
      ['RAG', '2026-12-08'],
      ['RAG', '2026-12-10'],
    ].map(([project, day]) => ({
      project, start: `${day}T18:00:00+01:00`, end: `${day}T20:00:00+01:00`,
    })),
  };
}

test('real approved plan has six correct sessions, 12 hours and four per project', () => {
  const result = checkPlan(realPlan());
  assert.equal(result.totalHours, 12);
  assert.deepEqual(result.sessions.map(({ start }) => start.slice(0, 10)), [
    '2026-11-24', '2026-11-26', '2026-12-01', '2026-12-03', '2026-12-08', '2026-12-10',
  ]);
  assert.ok(result.sessions.every(({ durationMinutes }) => durationMinutes === 120));
  assert.deepEqual(result.projects.map(({ hours }) => hours), [4, 4, 4]);
});

test('rejects the original two-week window because RAG does not fit', () => {
  const plan = realPlan();
  plan.endDate = '2026-12-06';
  assert.throws(() => checkPlan(plan), /outside the agreed window/);
});

test('rejects wrong effort, overlap, project order and unknown project', () => {
  let plan = realPlan();
  plan.projects[0].hours = 5;
  assert.throws(() => checkPlan(plan), /Effort mismatch/);
  plan = realPlan();
  plan.sessions[1] = { ...plan.sessions[0] };
  assert.throws(() => checkPlan(plan), /overlap/);
  plan = realPlan();
  plan.projects.reverse();
  assert.throws(() => checkPlan(plan), /project order/);
  plan = realPlan();
  plan.sessions[0].project = 'Unknown';
  assert.throws(() => checkPlan(plan), /unknown project/);
});

test('rejects invalid dates, zero duration, missing offsets and incorrect Rome offsets', () => {
  let plan = realPlan();
  plan.startDate = '2026-11-31';
  assert.throws(() => checkPlan(plan), /startDate is invalid/);
  plan = realPlan();
  plan.sessions[0].end = plan.sessions[0].start;
  assert.throws(() => checkPlan(plan), /positive/);
  plan = realPlan();
  plan.sessions[0].start = '2026-11-24T18:00:00';
  assert.throws(() => checkPlan(plan), /offset-aware/);
  plan = realPlan();
  plan.sessions[0].start = '2026-11-24T18:00:00+02:00';
  assert.throws(() => checkPlan(plan), /does not match timezone/);
});

test('accepts the Rome summer offset and rejects winter offset in summer', () => {
  const plan = {
    title: 'Summer plan', timezone: 'Europe/Rome',
    startDate: '2026-07-01', endDate: '2026-07-01',
    projects: [{ name: 'Backend', hours: 2 }],
    sessions: [{
      project: 'Backend', start: '2026-07-01T18:00:00+02:00', end: '2026-07-01T20:00:00+02:00',
    }],
  };
  assert.equal(checkPlan(plan).totalHours, 2);
  plan.sessions[0].start = '2026-07-01T18:00:00+01:00';
  assert.throws(() => checkPlan(plan), /does not match timezone/);
});

test('rejects invalid timezone, duplicate projects and malformed input', () => {
  const plan = realPlan();
  plan.timezone = 'not-a-timezone';
  assert.throws(() => checkPlan(plan), RangeError);
  const duplicate = realPlan();
  duplicate.projects.push({ name: 'Backend', hours: 4 });
  assert.throws(() => checkPlan(duplicate), /Duplicate project/);
  assert.throws(() => checkPlan(null), /plan object/);
  assert.throws(() => checkPlan({}), /Title/);
});

test('verifies a real-plan event with the documented omitted busy default', () => {
  const session = realPlan().sessions[0];
  const expected = {
    id: 'event-id', summary: 'Deep work - Backend (1/2)',
    description: 'Approved description', calendarId: 'test@example.invalid', session,
  };
  const event = {
    id: expected.id, status: 'confirmed', summary: expected.summary,
    description: expected.description, organizer: { email: expected.calendarId },
    start: { dateTime: session.start, timeZone: 'Europe/Madrid' },
    end: { dateTime: session.end, timeZone: 'Europe/Madrid' },
    visibility: 'private', reminders: { useDefault: false },
    htmlLink: 'https://www.google.com/calendar/event?eid=test',
  };
  assert.equal(checkCalendarEvent(event, expected).transparency, 'opaque');
  assert.equal(checkCalendarEvent(event, expected).durationMinutes, 120);
  assert.throws(() => checkCalendarEvent({ ...event, transparency: 'transparent' }, expected), /block time/);
  assert.throws(() => checkCalendarEvent({ ...event, reminders: { useDefault: true } }, expected), /reminders/);
  assert.throws(() => checkCalendarEvent({ ...event, attendeesOmitted: true }, expected), /attendees/);
  assert.throws(() => checkCalendarEvent({ ...event, recurringEventId: 'series' }, expected), /single session/);
  assert.throws(() => checkCalendarEvent({ ...event, hangoutLink: 'https://meet.google.com/test' }, expected), /conference/);
  assert.throws(() => checkCalendarEvent({ ...event, start: { dateTime: realPlan().sessions[1].start } }, expected), /start mismatch/);
});
