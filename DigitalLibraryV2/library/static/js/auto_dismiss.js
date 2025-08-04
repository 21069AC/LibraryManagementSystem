setTimeout(() => {
    document.querySelectorAll(".alert").forEach(alert => {
        alert.remove()
    });
}, 5000); // remove the alert after 5000 milliseconds (5 seconds)