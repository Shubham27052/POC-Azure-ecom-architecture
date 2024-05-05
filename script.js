  const nameInput = document.querySelector("#name");
  const email = document.querySelector("#email");
  const message = document.querySelector("#message");
  const file = document.getElementById("file")
  const form = document.querySelector("#form");


  const url =
    "https://poc-ecommerce-function.azurewebsites.net/api/http_trigger?";

  form.addEventListener("submit", function (event) {
    //preventing default submit
    event.preventDefault();

    // getting the input file
    const uploadedfile = file.files[0]
    const formData = new FormData()
    formData.append('uploadedfile', uploadedfile)
    console.log(formData.get("uploadedfile"))

    //defining the request body
    var request_body = {
      name: nameInput.value,
      email: email.value,
      message: message.value,
      file: formData
    };

    console.log(request_body)

    //fetching the request
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request_body),
    })
      
      .then((response) => {
          if (response.status === 200) {
            document.getElementById("final-message").style.display = "block";
            document.getElementById("form").style.display = "none";
            document.getElementById("final-message-h3").innerHTML = "Form filled successfully";
            console.log(response)
            return {"message":"success"}
          } else {
            document.getElementById("form").reset();
            document.getElementById("final-message-h3").innerHTML = "Error Occured while submitting the form. Please Try again";
            document.getElementById("final-message").style.display = "block";
            document.getElementById("final-message").style.margin = "20px auto";
            document.getElementById("form").style.margin = "3vh auto 3vh auto";
            document.getElementById("form").style.padding = "20px 30px";
            console.log(response)
            return {"message":"Failed"}
          }
          
      })  
      .then((data) => {
        console.log(data);
      });
    });

  
