const $ = (selector, parent = document) => {
  return parent.querySelector(selector);
};
const $$ = (selector, parent = document) => {
  return Array.from(parent.querySelectorAll(selector));
};

function debounce(func, wait) {
  let timeout;
  return function (...args) {
    const later = () => {
      clearTimeout(timeout);
      func.apply(this, args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

$$(".rich-text a").forEach((link) => {
  link.setAttribute("target", "_blank");
  link.setAttribute("rel", "noopener noreferrer");
});

const baseMaterial = $(".exercise-base-material-component");
const pageID = baseMaterial.dataset.id;
const questions = $$(".question", baseMaterial);
const csrfToken = $("[name='csrfmiddlewaretoken']").value;

function updateNextPageButtonState() {
  const nextPageLink = $(".next-page-button a", baseMaterial);
  if (!nextPageLink) {
    return;
  }
  const allAnswered = questions.every((question) =>
    question.classList.contains("answered"),
  );
  if (allAnswered) {
    nextPageLink.removeAttribute("aria-disabled");
  } else {
    nextPageLink.setAttribute("aria-disabled", "true");
  }
}

updateNextPageButtonState();

function scrollToElementIfNeeded(element) {
  // scroll element in to view if top of the element is less than 15%
  // from the bottom of the viewport
  const rect = element.getBoundingClientRect();
  if (rect.top > window.innerHeight * 0.85) {
    // scroll top of the element to the center of the viewport
    const scrollTop = rect.top + window.scrollY - window.innerHeight / 2;
    window.scrollTo({
      top: scrollTop,
      behavior: "smooth",
    });
  }
}

function drawDebugSquare(x, y, color) {
  const debugSquare = document.createElement("div");
  debugSquare.style.width = "10px";
  debugSquare.style.height = "10px";
  debugSquare.style.backgroundColor = color;
  debugSquare.style.position = "absolute";
  debugSquare.style.left = `${x - 5}px`;
  debugSquare.style.top = `${y - 5}px`;
  debugSquare.style.zIndex = "1000";
  document.body.appendChild(debugSquare);
}

function connectTwoAnswers(question, option1, option2, color) {
  option1.classList.remove("selected");
  option2.classList.remove("selected");
  option1.classList.add("connected");
  option2.classList.add("connected");
  option1.dataset.connectedIndex = option2.dataset.index;
  option2.dataset.connectedIndex = option1.dataset.index;

  const rect1 = option1.getBoundingClientRect();
  const rect2 = option2.getBoundingClientRect();

  // coordinates of the left and right edge at the center of height for the
  // options including page scroll
  let p1;
  let p2;
  if (rect1.left < rect2.left) {
    const x1 = rect1.right + window.scrollX;
    const y1 = rect1.top + rect1.height / 2 + window.scrollY;
    const x2 = rect2.left + window.scrollX;
    const y2 = rect2.top + rect2.height / 2 + window.scrollY;
    p1 = { x: x1, y: y1 };
    p2 = { x: x2, y: y2 };
  } else {
    const x1 = rect2.right + window.scrollX;
    const y1 = rect2.top + rect2.height / 2 + window.scrollY;
    const x2 = rect1.left + window.scrollX;
    const y2 = rect1.top + rect1.height / 2 + window.scrollY;
    p1 = { x: x2, y: y2 };
    p2 = { x: x1, y: y1 };
  }
  if (p1.y > p2.y) {
    [p1, p2] = [p2, p1];
  }

  // add debug squares at the centers of the options
  // drawDebugSquare(p1.x, p1.y, "red");
  // drawDebugSquare(p2.x, p2.y, "blue");

  // draw a line between the options using svg
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.style.position = "absolute";
  const top = p1.y > p2.y ? p2.y : p1.y;
  const left = p1.x < p2.x ? p1.x : p2.x;
  const width = Math.abs(p2.x - p1.x);
  const height = Math.abs(p2.y - p1.y);
  svg.style.left = `${left - 5}px`;
  svg.style.top = `${top - 5}px`;
  svg.style.width = `${width + 10}px`;
  svg.style.height = `${height + 10}px`;
  svg.style.pointerEvents = "none";
  svg.style.zIndex = "1";
  svg.classList.add("connection");
  question.appendChild(svg);

  // curved line
  const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
  const cp1 = { x: (p1.x + p2.x) / 2, y: p1.y };
  const cp2 = { x: (p1.x + p2.x) / 2, y: p2.y };
  // drawDebugSquare(cp1.x, cp1.y, "green");
  // drawDebugSquare(cp2.x, cp2.y, "orange");
  const d = `
    M ${p1.x - left + 5} ${p1.y - top + 5}
    C ${cp1.x - left + 5} ${cp1.y - top + 5},
      ${cp2.x - left + 5} ${cp2.y - top + 5},
      ${p2.x - left + 5} ${p2.y - top + 5}
  `;
  path.setAttribute("d", d);
  path.setAttribute("stroke", color);
  path.setAttribute("stroke-width", "4");
  path.setAttribute("fill", "none");
  svg.appendChild(path);
}

function drawConnections(question) {
  $$("svg.connection", question).forEach((svg) => svg.remove());

  const answered = question.classList.contains("answered");

  const leftOptions = $$(
    ".connect-two-answers-left .connect-two-answers-option",
    question,
  );
  leftOptions.forEach((leftOption) => {
    const connectedIndex = leftOption.dataset.connectedIndex;
    if (connectedIndex) {
      const rightOption = $(
        `.connect-two-answers-right .connect-two-answers-option[data-index="${connectedIndex}"]`,
        question,
      );
      if (rightOption) {
        let color = "var(--color-purple)";
        if (answered) {
          color = "var(--color-green)";
        }
        if (
          answered &&
          leftOption.dataset.index !== rightOption.dataset.index
        ) {
          const rightCorrectOption = $(
            `.connect-two-answers-right .connect-two-answers-option[data-index="${leftOption.dataset.index}"]`,
            question,
          );
          connectTwoAnswers(
            question,
            leftOption,
            rightCorrectOption,
            "var(--color-green-lighter)",
          );
          color = "var(--color-error)";
        }
        connectTwoAnswers(question, leftOption, rightOption, color);
      }
    }
  });
}

const debouncedDrawConnections = debounce(drawConnections, 200);

if (!questions.length) {
  // submit an empty answer to mark the page as completed
  submitAnswer(null, null, []);
} else {
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
      if (type === "connect_two_answers_question") {
        window.addEventListener("load", () => {
          drawConnections(question);
        });
        window.addEventListener("resize", () => {
          debouncedDrawConnections(question);
        });
      }
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
    } else if (type === "order_by_priority_question") {
      question.__sortable = new Sortable(answers);
      answerSelected = true;
      updateSubmitButtonState();
    } else if (type === "connect_two_answers_question") {
      const options = $$(".connect-two-answers-option", answers);
      const onClick = (event) => {
        const option = event.currentTarget;
        if (option.classList.contains("selected")) {
          option.classList.remove("selected");
        } else if (!option.classList.contains("connected")) {
          option.classList.add("selected");
        }
        const sameList = option.closest(".connect-two-answers-list");
        $$(".connect-two-answers-option.selected", sameList).forEach((opt) => {
          if (opt !== option) {
            opt.classList.remove("selected");
          }
        });
        if (option.classList.contains("selected")) {
          const otherList = $$(
            ".connect-two-answers-list",
            sameList.parentElement,
          ).filter((list) => list !== sameList)[0];
          if (otherList) {
            const otherOption = $(
              ".connect-two-answers-option.selected",
              otherList,
            );
            if (otherOption) {
              connectTwoAnswers(
                question,
                option,
                otherOption,
                "var(--color-purple)",
              );
              answerSelected = false;
              const allConnected = $$(
                ".connect-two-answers-option",
                answers,
              ).every((opt) => opt.classList.contains("connected"));
              if (allConnected) {
                answerSelected = true;
              }
              updateSubmitButtonState();
            }
          }
        }
      };
      options.forEach((option) => {
        option.addEventListener("click", onClick);
      });
      window.addEventListener("resize", () => {
        debouncedDrawConnections(question);
      });
    }

    submitButton.addEventListener("click", () => {
      question.classList.add("answered");
      if (explanationText) {
        explanationText.classList.remove("hidden");
        scrollToElementIfNeeded(explanationText);
      }
      disableQuestion();
      submitAnswer(question, type, inputs);
    });
  });
}

function showCorrectOrder(question, value) {
  const options = $$(".priority-option", question);
  options.forEach((option, index) => {
    const correct = Number(option.dataset.order);
    const answered = index;
    if (correct === answered) {
      option.classList.add("correct");
    }
  });
}

async function submitAnswer(question, type, inputs) {
  let value = null;
  let questionID = null;

  if (question) {
    questionID = question.dataset.questionId;

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
    } else if (type === "order_by_priority_question") {
      const optionElements = $$(".priority-option", question);
      value = optionElements.map((el) => parseInt(el.dataset.order));
      question.__sortable.destroy();
      showCorrectOrder(question, value);
    } else if (type === "connect_two_answers_question") {
      const leftOptions = $$(
        ".connect-two-answers-left .connect-two-answers-option",
        question,
      );
      const rightOptions = $$(
        ".connect-two-answers-right .connect-two-answers-option",
        question,
      );
      const connections = leftOptions.map((el) => {
        return [
          parseInt(el.dataset.index),
          parseInt(el.dataset.connectedIndex),
        ];
      });
      value = {
        left: leftOptions.map((el) => parseInt(el.dataset.index)),
        right: rightOptions.map((el) => parseInt(el.dataset.index)),
        connections: connections,
      };
      leftOptions.forEach((leftOption) => {
        if (leftOption.dataset.index === leftOption.dataset.connectedIndex) {
          leftOption.classList.add("correct");
        }
      });
      rightOptions.forEach((rightOption) => {
        if (rightOption.dataset.index === rightOption.dataset.connectedIndex) {
          rightOption.classList.add("correct");
        }
      });
      drawConnections(question);
    }

    if (!value) {
      return;
    }
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
