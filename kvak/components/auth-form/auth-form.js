(() => {
  // Find the select element with id 'id_country'
  const selectElem = document.querySelector("#id_country");
  if (!selectElem) return;
  const countries = Array.from(selectElem.options)
    .map((option) => [option.value, option.text])
    .filter(([value, text]) => value && text);

  // Create a new element structure to replace the select element
  const inputWrapperElem = document.createElement("div");
  inputWrapperElem.id = "autocomplete_country";
  inputWrapperElem.className = "autocomplete";

  const inputElem = document.createElement("input");
  inputElem.className = "autocomplete-input";
  inputWrapperElem.appendChild(inputElem);

  const hiddenInputElem = document.createElement("input");
  hiddenInputElem.type = "hidden";
  hiddenInputElem.id = selectElem.id;
  hiddenInputElem.name = selectElem.name;
  hiddenInputElem.required = selectElem.required;
  inputWrapperElem.appendChild(hiddenInputElem);

  if (selectElem.value) {
    hiddenInputElem.value = selectElem.value;
    const country = countries.find(([cCode]) => cCode === selectElem.value);
    if (country) {
      inputElem.value = country[1];
    }
  }

  const resultListElem = document.createElement("ul");
  resultListElem.className = "autocomplete-result-list";
  inputWrapperElem.appendChild(resultListElem);

  // Replace the select element with the new elements
  selectElem.replaceWith(inputWrapperElem);

  inputElem.addEventListener("change", (event) => {
    const inputValue = event.target.value;
    const country = countries.find(
      ([cCode, cName]) => cName.toLowerCase() === inputValue.toLowerCase()
    );
    if (country) {
      hiddenInputElem.value = country[0];
    } else {
      hiddenInputElem.value = "";
    }
  });

  // Initialize the autocomplete functionality
  new Autocomplete(inputWrapperElem, {
    autoSelect: true,
    search: (input) => {
      if (input.length < 1) {
        return countries;
      }
      return countries.filter(([cCode, cName]) => {
        return cName.toLowerCase().startsWith(input.toLowerCase());
      });
    },
    getResultValue: ([cCode, cName]) => {
      return cName;
    },
    onSubmit: ([cCode, cName]) => {
      hiddenInputElem.value = cCode;
    },
  });
})();
