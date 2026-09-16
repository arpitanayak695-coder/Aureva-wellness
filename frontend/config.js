
window.AUREVA_CONFIG = {
  API_BASE_LOCAL: "http://127.0.0.1:8000",
  API_BASE_PRODUCTION: "https://REPLACE-WITH-YOUR-BACKEND-URL"
};

window.AUREVA_API_BASE = (function () {
  var host = window.location.hostname;
  var isLocal =
    host === "localhost" ||
    host === "127.0.0.1" ||
    host === "0.0.0.0" ||
    host === "" ||                      
    /^192\.168\./.test(host) ||
    /^10\./.test(host);
  return isLocal
    ? window.AUREVA_CONFIG.API_BASE_LOCAL
    : window.AUREVA_CONFIG.API_BASE_PRODUCTION;
})();
