"use strict";

(function () {
  window.addEventListener("load", init);
  function init() {
    const values = document.querySelectorAll("input.checkbox");
    // Checks if the box is ticked or not on the backend
    fetch('/get_check_status')
      .then(statusCheck)
      .then((data) => {
        data.forEach((id) => {
          console.log(id);
          const target = document.getElementById(id);
          if (target !== null) target.checked = true;
        });
      })
    values.forEach((value) => {
      value.addEventListener("change", function (e) {
        if (e.currentTarget.checked) {
          // TODO add the image to the backend
          const id = value.getAttribute("id");
          fetch('/add_relevance/' + id)
            .then(statusCheck)
            .then(console.log)
        } else {
          // TODO remove the image from the backend
          const id = value.getAttribute("id");
          fetch('/remove_relevance/' + id)
            .then(statusCheck)
            .then(console.log)
        }
      });
    });
  }

  /**
   * Status check for the fetch request
   * @param {JSON} res - Response of the fetch request
   * @returns the results json if it succeeds, else error
   */
  function statusCheck(res) {
    if (res.ok) {
      return res.json();
    } else {
      return Error(res.statusText);
    }
  }
})();
