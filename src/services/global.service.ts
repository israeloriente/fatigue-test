import Swal from "sweetalert2";
import type { SimpleAlert } from "../interfaces/alert.interface";
import { i18n } from "../main";

namespace GlobalService {
  export function setStorage(key: string, value: any) {
    if (typeof value == "string") {
      const keySplited = key.split(".");

      let data: any = localStorage.getItem(keySplited[0]);
      if (data) {
        data = JSON.parse(data);
        for (let i = 1; i < keySplited.length - 1; i++) {
          data = data[keySplited[i]];
        }
        data[keySplited[keySplited.length - 1]] = value;
        localStorage.setItem(keySplited[0], JSON.stringify(data));
      } else {
        let obj: any = {};
        for (let i = keySplited.length - 1; i > 0; i--) {
          const newObj: any = {};
          newObj[keySplited[i]] = value;
          value = newObj;
          obj = newObj;
        }
        localStorage.setItem(keySplited[0], JSON.stringify(obj));
      }
    }
  }

  export function getStorage(key: string) {
    const keySplited = key.split(".");
    let data: any = localStorage.getItem(keySplited[0]);
    if (data) {
      data = JSON.parse(data);
      for (let i = 1; i < keySplited.length; i++) {
        data = data[keySplited[i]];
      }
    }
    return data;
  }

  export function resetStorage(key: string) {
    localStorage.removeItem(key);
  }

  export function simpleAlert(route: string) {
    const alert: any = i18n.global.tm(route);
    Swal.fire(alert);
  }

  export function simpleToast(route: string) {
    const alert: string = i18n.global.t(route);
    Swal.fire({
      toast: true,
      position: "top-end",
      showConfirmButton: false,
      timer: 3000,
      timerProgressBar: false,
      icon: "success",
      title: alert,
    });
  }
}

export default GlobalService;
