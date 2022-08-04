function checkCompleteness(e) {
  // check if options have been selected
  if ($("input[name=yes_or_no]:checked").length < 1) {
    e.preventDefault();
  }
}

$("form").on("submit", checkCompleteness);
