import http from 'k6/http';
import { check, sleep, randomSeed } from 'k6';

randomSeed(1234);

export const options = {
  scenarios: {
    user_creation: {
      executor: 'constant-vus',
      vus: 50,
      duration: '20s',
    },
  },
};

const BASE_URL = 'http://localhost:8080/api';

function createUser(randomValue) {
  const username = `user${randomValue}`;
  const payload = JSON.stringify({
    email: `${username}@example.com`,
    password: 'password123',
    username: username,
    display_name: `User ${randomValue}`,
    is_admin: false,
  });
  const headers = { 'Content-Type': 'application/json' };
  return http.post(`${BASE_URL}/signup`, payload, { headers });
}

function loginUser(username) {
  const payload = `grant_type=&username=${username}&password=password123&scope=&client_id=&client_secret=`;
  const headers = { 'Content-Type': 'application/x-www-form-urlencoded' };
  return http.post(`${BASE_URL}/token`, payload, { headers });
}

function createTask(token, randomValue) {
  const payload = JSON.stringify({
    title: `Task for user${randomValue}`,
    detail: `Details for user${randomValue}'s task.`,
    id: `task_${randomValue}`,
  });
  const headers = {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
  };
  return http.post(`${BASE_URL}/task`, payload, { headers });
}

function getTaskDetail(token, taskId) {
  const headers = { Authorization: `Bearer ${token}` };
  return http.get(`${BASE_URL}/task/${taskId}`, { headers });
}

export default function () {
  const randomValue = Math.floor(Math.random() * 1000000);

  const signupRes = createUser(randomValue);
  check(signupRes, { 'User created successfully': (res) => res.status === 201 });

  const loginRes = loginUser(`user${randomValue}`);
  check(loginRes, { 'Login successful': (res) => res.status === 200 });

  const tokens = loginRes.json();
  const accessToken = tokens ? tokens.access_token : null;
  check(accessToken, { 'Access token is not null': (token) => token !== null });

  const taskRes = createTask(accessToken, randomValue);
  check(taskRes, { 'Task created successfully': (res) => res.status === 201 });

  const taskId = `task_${randomValue}`;

  const taskDetailRes = getTaskDetail(accessToken, taskId);
  check(taskDetailRes, { 'Task details fetched successfully': (res) => res.status === 200 });

  sleep(1);
}