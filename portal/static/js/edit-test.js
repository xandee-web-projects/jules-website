$(document).ready(function () {
  var questions = document.getElementById("questions");
  var addQuestion = document.getElementById("add_question");
  const questionTemplate = document.querySelector("[question-template]");
  const optionTemplate = document.querySelector("[option-template]");
  
  addQuestion.addEventListener("click", () => {
    let newQuestion = questionTemplate.content.cloneNode(true).children[0];
    const idx = questions.childElementCount + 1;
    newQuestion.setAttribute("questionNumber", idx);
    newQuestion.querySelector("input[type=text]").setAttribute("name", idx);
    questions.append(newQuestion);
    newQuestion
      .querySelector(".q-delete-btn")
      .addEventListener("click", (e) => newQuestion.remove());
    addOptionListener(newQuestion.querySelector(".add_option"));
  })

  function addOptionListener(optionBtn) {
    optionBtn.addEventListener("click", (e) => {
      let newOption = optionTemplate.content.cloneNode(true).children[0];
      const idx = `${optionBtn.parentElement.getAttribute("questionNumber")}-${optionBtn.previousElementSibling.childElementCount + 1}`;
      optionBtn.previousElementSibling.append(newOption);
      newOption.setAttribute("optionNumber", idx);
      newOption.querySelector("input[type=text]").setAttribute("name", idx);
      newOption.querySelector(".q-delete-btn").addEventListener("click", (e) => newOption.remove());
      const choose_ansBtn = newOption.querySelector(".choose-ans");
      choose_ansBtn.addEventListener("click", addChooseAnswer)
    });
  }
  
  function addChooseAnswer(e) {
      let questionOptions = this.parentElement.parentElement.parentElement.children;
      for (let i = 0; i < questionOptions.length; i++) {
        questionOptions[i].querySelector(".choose-ans").setAttribute("hidden", "true");
        questionOptions[i].querySelector(".q-delete-btn").setAttribute("disabled", "true");
        questionOptions[i].querySelector("i").innerHTML = "done_outline";
      }
      this.removeAttribute("hidden");
      this.querySelector("i").innerHTML = "check_circle";
      this.removeEventListener("click", addChooseAnswer)
      this.addEventListener("click", addRemoveAnswer)
  }
  
  function addRemoveAnswer(e) {
      let questionOptions = this.parentElement.parentElement.parentElement.children;
      for (let i = 0; i < questionOptions.length; i++) {
        questionOptions[i].querySelector(".choose-ans").removeAttribute("hidden");
        questionOptions[i].querySelector(".q-delete-btn").removeAttribute("disabled");
        questionOptions[i].querySelector("i").innerHTML = "done_outline";
      }
      this.querySelector("i").innerHTML = "done_outline";
      this.removeEventListener("click", addRemoveAnswer)
      this.addEventListener("click", addChooseAnswer)
  }
  var qs = document.querySelectorAll("[questionNumber]")
  var opts = document.querySelectorAll("[optionNumber]")
  for (let i = 0; i < qs.length; i++) {
    qs[i]
      .querySelector(".q-delete-btn")
      .addEventListener("click", (e) => qs[i].remove());
    addOptionListener(qs[i].querySelector(".add_option"));
  }
  for (let i = 0; i < opts.length; i++) {
    opts[i].querySelector(".q-delete-btn").addEventListener("click", (e) => opts[i].remove());
    const choose_ansBtn = opts[i].querySelector(".choose-ans");
    if (choose_ansBtn.querySelector("i").innerHTML == "done_outline"){
      choose_ansBtn.addEventListener("click", addChooseAnswer)
    }
    else {
      choose_ansBtn.addEventListener("click", addRemoveAnswer)
    }
  }
  $("#form").submit(function (e) { 
    e.preventDefault();
    const choose_ans = e.target.querySelectorAll(".choose-ans:not([hidden])")
    for (let i = 0; i < choose_ans.length; i++) {
      if (choose_ans[i].querySelector("i").innerHTML == "check_circle"){
        choose_ans[i].previousElementSibling.name += "-ans"
      }
    }
    e.target.submit()
  });
  
  $("#close-test").click((e) => {
    e.preventDefault();
    let c = confirm("Are you sure you want to close without saving?")
    if (c) return;
    e.target.click()
  })
  $("#publish").click((e) => {
    $("#form").append("<input type='hidden' name='publish' value='true'>")
    $("#form").submit()
  })
});


