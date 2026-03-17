export class Html5Qrcode {
  start() {
    return Promise.reject(new Error("Camera not available in Storybook"));
  }
  stop() {
    return Promise.resolve();
  }
  clear() {}
}
