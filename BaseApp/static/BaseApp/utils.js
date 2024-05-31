function refresh_page() {
  window.location.reload();
}

function redirect_to_url(url) {
  window.location.href = url;
}

function apply_hidden_to_element(element_id, other_element_id = null) {
  let element = document.getElementById(element_id);
  element.classList.add("hidden");
  if (other_element_id != null) {
    let other_element = document.getElementById(other_element_id);
    other_element.classList.add("hidden");
  }
}
