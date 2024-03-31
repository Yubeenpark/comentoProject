let DEBUG = false;
let HOST_URL = "http://ec2-3-34-90-91.ap-northeast-2.compute.amazonaws.com:8000/";
let SOCKET_URL = "wss://http://ec2-3-34-90-91.ap-northeast-2.compute.amazonaws.com:8000/";
if (DEBUG) {
  HOST_URL = "http://127.0.0.1:8000";
  SOCKET_URL = "ws://127.0.0.1:8000";
}

export { HOST_URL, SOCKET_URL };
