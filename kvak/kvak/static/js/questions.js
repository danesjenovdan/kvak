const $ = (selector, parent = document) => {
  return parent.querySelector(selector);
};
const $$ = (selector, parent = document) => {
  return Array.from(parent.querySelectorAll(selector));
};

const baseMaterial = $(".exercise-base-material-component");
const pageID = baseMaterial.dataset.id;
const questions = $$(".question", baseMaterial);
const csrfToken = $("[name='csrfmiddlewaretoken']").value;

function updateNextPageButtonState() {
  const nextPageLink = $(".next-page-button a", baseMaterial);
  console.log(nextPageLink);
  if (!nextPageLink) {
    return;
  }
  const allAnswered = questions.every((question) =>
    question.classList.contains("answered")
  );
  console.log("All answered:", allAnswered);
  if (allAnswered) {
    nextPageLink.removeAttribute("aria-disabled");
  } else {
    nextPageLink.setAttribute("aria-disabled", "true");
  }
}

updateNextPageButtonState();

questions.forEach((question) => {
  const submitContainer = $(".answer-submit", question);
  const submitButton = $(".answer-submit button", question);
  const explanationText = $(".explanation-text", question);
  const answers = $(".answers", question);
  const inputs = $$("input, textarea", answers);
  const type = answers.dataset.questionType;

  const disableQuestion = () => {
    submitButton.setAttribute("disabled", "disabled");
    submitContainer.classList.add("hidden");
    inputs.forEach((input) => {
      input.setAttribute("disabled", "disabled");
    });
    updateNextPageButtonState();
  };

  if (question.classList.contains("answered")) {
    disableQuestion();
    return;
  }

  let answerSelected = false;

  const updateSubmitButtonState = () => {
    if (answerSelected) {
      submitButton.removeAttribute("disabled");
    } else {
      submitButton.setAttribute("disabled", "disabled");
    }
  };

  if (type === "one_correct_answer_question") {
    const options = $$(".answer-option input[type='radio']", answers);
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
  } else if (type === "multiple_choice_question") {
    const options = $$(".answer-option input[type='checkbox']", answers);
    const onChange = () => {
      answerSelected = Array.from(options).some((opt) => opt.checked);
      updateSubmitButtonState();
    };
    options.forEach((option) => {
      option.addEventListener("change", onChange);
    });
    onChange();
  } else if (type === "text_answer_question") {
    const textarea = $("textarea", answers);
    const onInput = () => {
      answerSelected = textarea.value.trim().length > 0;
      updateSubmitButtonState();
    };
    textarea.addEventListener("input", onInput);
    onInput();
  }

  submitButton.addEventListener("click", () => {
    question.classList.add("answered");
    explanationText.classList.remove("hidden");
    disableQuestion();
    submitAnswer(question, type, inputs);
  });
});

async function submitAnswer(question, type, inputs) {
  const questionID = question.dataset.questionId;

  let value = null;
  if (type === "one_correct_answer_question") {
    const selectedOption = inputs.find((input) => input.checked);
    value = selectedOption ? selectedOption.value : null;
  } else if (type === "multiple_choice_question") {
    const selectedOptions = inputs
      .filter((input) => input.checked)
      .map((input) => input.value);
    value = selectedOptions;
  } else if (type === "text_answer_question") {
    const answer = inputs.find((input) => input.tagName === "TEXTAREA");
    value = answer ? answer.value : null;
  }

  if (!value) {
    return;
  }

  const answerData = {
    page_id: pageID,
    question_id: questionID,
    answer: value,
  };

  const response = await fetch("/api/answer/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify(answerData),
  });
}
