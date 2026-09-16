/* ==========================================================================
   Aureva Wellness — contact form.
   Flow: collect → client-side check → POST /api/contact → render result.
   The backend is the authority; these checks only save the user a round trip.
   ========================================================================== */
(function () {
  "use strict";

  var form = document.getElementById("contactForm");
  if (!form) return;

var API_BASE = (window.AUREVA_CONFIG && window.AUREVA_CONFIG.API_BASE_PRODUCTION) || "https://aureva-backend.vercel.app";
var ENDPOINT = API_BASE.replace(/\/+$/, "") + "/api/contact";

  var submitBtn = document.getElementById("submitBtn");
  var btnLabel = submitBtn.querySelector(".btn-label");
  var alertBox = document.getElementById("formAlert");
  var successBox = document.getElementById("formSuccess");
  var sendAnother = document.getElementById("sendAnother");
  var messageEl = document.getElementById("message");
  var messageCount = document.getElementById("messageCount");

  var FIELDS = [
    "full_name", "mobile", "email", "program",
    "preferred_date", "preferred_time", "message"
  ];

  var LABELS = {
    full_name: "full name",
    mobile: "mobile number",
    email: "email address",
    program: "programme",
    preferred_date: "preferred date",
    preferred_time: "preferred time",
    message: "message"
  };

  var busy = false;

  /* ---------------------------------------------------------------- utils */
  function input(name) {
    return form.elements[name];
  }

  function setFieldError(name, text) {
    var el = input(name);
    if (!el) return;
    var wrap = el.closest(".field");
    var slot = document.getElementById("error-" + name);
    if (slot) slot.textContent = text || "";
    if (wrap) wrap.classList.toggle("has-error", Boolean(text));
    el.setAttribute("aria-invalid", text ? "true" : "false");
  }

  function clearErrors() {
    FIELDS.forEach(function (name) { setFieldError(name, ""); });
    alertBox.hidden = true;
    alertBox.textContent = "";
  }

  function showAlert(text) {
    alertBox.textContent = text;
    alertBox.hidden = false;
    alertBox.scrollIntoView({ block: "nearest" });
  }

  function values() {
    var data = {};
    FIELDS.forEach(function (name) {
      var el = input(name);
      data[name] = el ? String(el.value).trim() : "";
    });
    return data;
  }

  function setLoading(state) {
    busy = state;
    submitBtn.disabled = state;
    submitBtn.classList.toggle("is-loading", state);
    btnLabel.textContent = state ? "Sending…" : "Send request";
  }

  /* --------------------------------------------------- client-side checks */
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[A-Za-z]{2,}$/;
  var PHONE_RE = /^[+(]?[0-9][0-9\s\-()]{7,19}$/;

  function validate(data) {
    var errors = {};

    FIELDS.forEach(function (name) {
      if (!data[name]) {
        errors[name] = "Please enter your " + LABELS[name] + ".";
      }
    });

    if (!errors.full_name && (data.full_name.length < 2 || data.full_name.length > 80)) {
      errors.full_name = "Your name should be between 2 and 80 characters.";
    }
    if (!errors.mobile && !PHONE_RE.test(data.mobile)) {
      errors.mobile = "Please enter a valid mobile number, for example +91 90000 00000.";
    }
    if (!errors.email && !EMAIL_RE.test(data.email)) {
      errors.email = "Please enter a valid email address.";
    }
    if (!errors.program) {
      errors.program = undefined;
      delete errors.program;
    }
    if (!errors.preferred_date && !/^\d{4}-\d{2}-\d{2}$/.test(data.preferred_date)) {
      errors.preferred_date = "Please choose a date in the format YYYY-MM-DD.";
    }
    if (!errors.preferred_time && !/^\d{2}:\d{2}(:\d{2})?$/.test(data.preferred_time)) {
      errors.preferred_time = "Please choose a time.";
    }
    if (!errors.message && (data.message.length < 10 || data.message.length > 1000)) {
      errors.message = "Please write between 10 and 1000 characters.";
    }
    return errors;
  }

  function paintErrors(errors) {
    var first = null;
    FIELDS.forEach(function (name) {
      var text = errors[name] || "";
      setFieldError(name, text);
      if (text && !first) first = input(name);
    });
    if (first) first.focus();
  }

  /* -------------------------------------------------------------- submit */
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    if (busy) return;                       // blocks double submission

    clearErrors();
    var data = values();
    var errors = validate(data);

    if (Object.keys(errors).length) {
      paintErrors(errors);
      showAlert("Please correct the highlighted fields.");
      return;
    }

    send(data);
  });

  function send(data) {
    setLoading(true);

    var controller = typeof AbortController !== "undefined" ? new AbortController() : null;
    var timer = controller ? window.setTimeout(function () { controller.abort(); }, 20000) : null;

    fetch("https://aureva-backend.vercel.app/api/contact",{
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify(data),
      signal: controller ? controller.signal : undefined
    })
      .then(function (response) {
        return response.json()
          .catch(function () { return {}; })
          .then(function (body) { return { status: response.status, body: body }; });
      })
      .then(function (result) {
        var body = result.body || {};

        if (result.status === 200 && body.success) {
          onSuccess();
          return;
        }

        if (result.status === 400 || result.status === 422) {
          if (body.errors && typeof body.errors === "object") paintErrors(body.errors);
          showAlert(body.message || "Please correct the highlighted fields.");
          return;
        }

        if (result.status === 405) {
          showAlert("That request method is not allowed. Please reload the page and try again.");
          return;
        }

        if (result.status === 429) {
          showAlert(body.message || "Too many requests from this device. Please try again in a few minutes.");
          return;
        }

        showAlert(body.message ||
          "We could not send your request just now. Please try again in a moment, " +
          "or email hello@aureva.example.");
      })
      .catch(function (error) {
        if (error && error.name === "AbortError") {
          showAlert("The request timed out. Please check your connection and try again.");
        } else {
          showAlert("We could not reach the studio server. Check that the backend is running, " +
            "then try again — or email hello@aureva.example.");
        }
      })
      .then(function () {
        if (timer) window.clearTimeout(timer);
        setLoading(false);
      });
  }

  function onSuccess() {
    form.reset();                           // reset only after a real success
    if (messageCount) messageCount.textContent = "0";
    clearErrors();
    form.hidden = true;
    successBox.hidden = false;
    successBox.scrollIntoView({ behavior: "smooth", block: "center" });
    var heading = successBox.querySelector("h3");
    if (heading) {
      heading.setAttribute("tabindex", "-1");
      heading.focus();
    }
  }

  if (sendAnother) {
    sendAnother.addEventListener("click", function () {
      successBox.hidden = true;
      form.hidden = false;
      var first = input("full_name");
      if (first) first.focus();
    });
  }

  /* ------------------------------------------------- small conveniences */
  if (messageEl && messageCount) {
    messageEl.addEventListener("input", function () {
      messageCount.textContent = String(messageEl.value.length);
    });
  }

  // Clear a field's error as soon as the user edits it.
  FIELDS.forEach(function (name) {
    var el = input(name);
    if (!el) return;
    el.addEventListener("input", function () { setFieldError(name, ""); });
    el.addEventListener("change", function () { setFieldError(name, ""); });
  });

  // Today is the earliest bookable date.
  var dateEl = input("preferred_date");
  if (dateEl && !dateEl.min) {
    var now = new Date();
    var iso = now.getFullYear() + "-" +
      String(now.getMonth() + 1).padStart(2, "0") + "-" +
      String(now.getDate()).padStart(2, "0");
    dateEl.min = iso;
  }
})();
