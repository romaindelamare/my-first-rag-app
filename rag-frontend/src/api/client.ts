import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000/api",
  timeout: 15000,
});

API.interceptors.response.use(
  (res) => res,
  (err) => {
    console.error("API Error:", err);
    return Promise.reject(err);
  }
);

export default API;
