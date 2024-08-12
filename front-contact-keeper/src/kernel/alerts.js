import SweetAlert from "sweetalert2";

export const onError = async (title, text) => {
    await SweetAlert.fire({
        icon: 'error',
        title: title,
        text: text
    })
}

export const onWarning = async (title, text) => {
    await SweetAlert.fire({
        icon: 'warning',
        title: title,
        text: text
    })
}

export const onQuestion = async (title, text) => {
    return await SweetAlert.fire({
        icon: 'question',
        title: title,
        text: text,
        showCancelButton: true,
        confirmButtonColor: '#000',
        cancelButtonColor: '#333',
        confirmButtonText: 'Aceptar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        return result.isConfirmed
    })
}

export const onSuccess = async (title, text) => {
    await SweetAlert.fire({
        icon: 'success',
        title: title,
        text: text
    })
}



export const onToast = (title, text, icon) => {
    const Toast = SweetAlert.mixin({
        toast: true,
        position: "top-end",
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didOpen: (toast) => {
          toast.onmouseenter = SweetAlert.stopTimer;
          toast.onmouseleave = SweetAlert.resumeTimer;
        }
      });
    Toast.fire({
        icon,
        title,
        text
    });
      
}