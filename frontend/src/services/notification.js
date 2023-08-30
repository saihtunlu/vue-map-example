export default class Notification {
  constructor(notification) {
    this.notification = notification;
  }

  /**
   * displaying notification message
   * @param {String} message Message body
   * @param {String} title title of notification
   * @param {String} status status of notification
   * @param {String} color color of notification
   *
   */
  display(message, title, status = "normal", color = "success") {
    if (status === "error") {
      if (
        typeof message.response.data === "object" &&
        !message.response.data.byteLength
      ) {
        for (var key in message.response.data) {
          this.notification({
            color: color,
            title: key,
            text:
              typeof message.response.data[key] === "string"
                ? message.response.data[key]
                : message.response.data[key][0],
          });
        }
      } else {
        this.notification({
          color: color,
          title: "status - " + message.response.status,
          text: message.response.statusText,
        });
      }
    } else if (status === "normal") {
      this.notification({
        color: color,
        title: title,
        text: message,
      });
    }
  }
}
