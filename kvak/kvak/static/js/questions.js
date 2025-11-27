const questions = document.querySelectorAll(
  ".exercise-base-material-component .question"
);

questions.forEach((question) => {
  const submitButton = question.querySelector(".asnwer-submit button");
  const explanationText = question.querySelector(".explanation-text");
  const answerType = question.querySelector(".answers").dataset.questionType;
  let answerSelected = false;

  const updateSubmitButtonState = () => {
    if (answerSelected) {
      submitButton.removeAttribute("disabled");
    } else {
      submitButton.setAttribute("disabled", "true");
    }
  };

  if (answerType === "one_correct_answer_question") {
    const options = question.querySelectorAll(
      ".answer-option input[type='radio']"
    );
    const onChange = () => {
      answerSelected = true;
      updateSubmitButtonState();
    };
    options.forEach((option) => {
      option.addEventListener("change", onChange);
    });
    const onLoad = () => {
      answerSelected = Array.from(options).some((opt) => opt.checked);
      updateSubmitButtonState();
    };
    onLoad();
  } else if (answerType === "multiple_choice_question") {
    const options = question.querySelectorAll(
      ".answer-option input[type='checkbox']"
    );
    const onChange = () => {
      answerSelected = Array.from(options).some((opt) => opt.checked);
      updateSubmitButtonState();
    };
    options.forEach((option) => {
      option.addEventListener("change", onChange);
    });
    onChange();
  } else if (answerType === "text_answer_question") {
    const textarea = question.querySelector(".answers textarea");
    const onInput = () => {
      answerSelected = textarea.value.trim().length > 0;
      updateSubmitButtonState();
    };
    textarea.addEventListener("input", onInput);
    onInput();
  }

  submitButton.addEventListener("click", () => {
    explanationText.classList.remove("hidden");
    submitButton.setAttribute("disabled", "true");
    const inputs = question.querySelectorAll(
      ".answers input, .answers textarea"
    );
    inputs.forEach((input) => {
      input.setAttribute("disabled", "true");
    });
    question.classList.add("answered");
  });
});
