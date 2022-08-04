function checkCompleteness(e) {
  // check if options have been selected
  if ($("input[name=options]:checked").length < 1) {
    e.preventDefault();
  }
}

$("form").on("submit", checkCompleteness);
