

function Add_or_remove_from_cart(value) {
    var action = value.action
    var product_id = value.product_id
    var user = value.user
    console.log(user)
    if (value.user === 'AnonymousUser'){
        AddCookieItem(action , product_id)
    }else{
        UpdateUserOrder(action , product_id )
    }

}



function AddCookieItem(action , product_id) {
    if (action === 'add'){
        if (cart[product_id] == undefined){
            cart[product_id] = {'quantity' : 1}
            console.log(cart)
        }else {
            cart[product_id]['quantity'] +=1
        }
    }else {
        if (cart[product_id]['quantity'] <=1){
            delete cart[product_id]

        }else {
            cart[product_id]['quantity'] -=1
        }
    }
    console.log("cart" , cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domin=;path=/"
    location.reload()
}


function UpdateUserOrder(action , product_id ){
    fetch('/update_item/', {
        'method':'POST',
        'headers':{
            'Content-Type': 'application/json',
            'X-CSRFToken':csrftoken
        },
        body:JSON.stringify({'action':action , 'product_id' : product_id})
    }).then((response)=>{
        return response.json()
    }).then((data)=>{
        $("#order_item_in_cart").html(data.page_cart)
        console.log(data.order_items)
        $("#cart-total").html(data.order_items)

    })

}



var form = document.getElementById("form")



form.addEventListener('submit' , function (e) {
    e.preventDefault()
    document.getElementById("payment-info").classList.remove('hidden')
    document.getElementById("form-button").classList.add("hidden")
})

var btn = document.getElementById('make-payment')

// btn.addEventListener('click' , function (e) {
//     submitedFormData()
// })

function submitedFormData(){
    user_info = {
        'name' : null,
        'email':null,
        'total' :total
    }
    user_shipping = {
        'address ': null,
        'city':null,
        'state' : null,
        'zipcode' : null
    }
    if (shipping !='False'){
        user_shipping.address = form.address.value
        user_shipping.zipcode = form.zipcode.value
        user_shipping.city = form.city.value
        user_shipping.state = form.state.value
    }
    if (user === 'AnonymousUser'){
        user_info.email = form.email.value
        user_info.name = form.name.value
    }

    fetch('/process_order/', {
        'method':'POST',
        'headers':{
            'Content-Type': 'application/json',
            'X-CSRFToken':csrftoken
        },
        body:JSON.stringify({'user_info':user_info , 'user_shipping' : user_shipping})
    }).then((response)=>{
        return response.json()
    }).then((data)=>{
        cart = {}
        document.cookie = 'cart=' + JSON.stringify(cart) + ";domin=;path=/"
        window.location.href = 'http://127.0.0.1:8000'
        alert("Payment is done")

        // $("#order_item_in_cart").html(data.page_cart)
        // console.log(data.order_items)
        // $("#cart-total").html(data.order_items)

    })
}


function CheckUserName(){
    $.get('/check_username/' , {'username' : $('.username').val()}).then(response => {
      if (response.status === 'valid'){
          $('#head-id').html('Please enter a secure password')
          $('#step').html('3/4')
          $('.username-section').addClass("fold-up");
          $('.password-section').removeClass("folded");
          $("#head-id").css('color' , '#9facb6')
      }else {
          $("#head-id").html('username is already taken!')
          $("#head-id").css('color' , 'red')
      }
  })
}



function CheckUserNameLogin(){
    $.get('/check_username/' , {'username' : $('.username').val()}).then(response => {
      if (response.status === 'valid'){
          $('#head-id').html('This username does not exist!')
          $("#head-id").css('color' , 'red')

      }else {
          $('#step').html('2/2')
          $('.username-section').addClass("fold-up");
          $('.password-section').removeClass("folded");
          $("#head-id").css('color' , '#9facb6')
          $('#head-id').html('Please enter your password')

      }
  })
}



function CheckEmailFormat(){
    const validateEmail = (email) => {
      return email.match(
        /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      );
    };
  if (validateEmail($('.email').val())){
      let email = $('.email').val()
      fetch('/check_email/', {
            'method':'POST',
            'headers':{
                'Content-Type': 'application/json',
                'X-CSRFToken':csrftoken
            },
            body:JSON.stringify({'email':email})
        }).then(response => {
            return response.json()

      }).then(data => {
          if (data.status === 'valid'){
                $('#head-id').html('Please enter a valid username')
                $('#step').html('2/4')
                $('.email-section').addClass("fold-up");
                $('.username-section').removeClass("folded");
                $("#head-id").css('color' , '#9facb6')
            }else {
                $("#head-id").html('This email has already been registered!<br><a href="/login-page/">Do you want to login?</a>')
                $("#head-id").css('color' , 'red')
            }
      })

  }else {
      $("#head-id").css('color' , 'red')
  }
}

function CheckPassword(){
    const password = $('.password').val()
    const repeat_password = $('.repeat-password').val()
    if (password === repeat_password){
        const email = $(".email").val()
        const username = $(".username").val()
        const password = $(".password").val()
        fetch('/register/', {
            'method':'POST',
            'headers':{
                'Content-Type': 'application/json',
                'X-CSRFToken':csrftoken
            },
            body:JSON.stringify({'email':email , 'username' : username , 'password' : password})
        }).then(response => {
            return response.json()
        }).then(data => {
            if (data.status === 'success'){
                $('#step').html('<i>successful!</i>')
                $('#step').css('margin-left' , '34%')
                $('#step').css('color' , 'limegreen')
                $('#head-id').html('')
                $('header').css('box-shadow' , '0px 0px 50px 1.5px #50d01d')
                $('.success').css('box-shadow' , '0px 0px 50px 1.5px #50d01d')
                $('.repeat-password-section').addClass("fold-up");
                $('.success').css("marginTop", 0);
                setTimeout(()=>{location.href = '/login/'} , 3000)

            }
        })

    }else {
        $('#head-id').html('The entered password is not the same as the repeated password')
        $("#head-id").css('color' , 'red')
    }

}


function Login() {
    let username = $(".username").val()
    let password = $('.password').val()
    fetch('/login/', {
        'method':'POST',
        'headers':{
            'Content-Type': 'application/json',
            'X-CSRFToken':csrftoken
        },
        body:JSON.stringify({'username' : username , 'password' : password})
    }).then(response => {
        return response.json()
    }).then(data => {
        if (data.status === 'successful'){
            $('#step').html('<i>successful!</i>')
            $('#step').css('margin-left' , '34%')
            $('#step').css('color' , 'limegreen')
            $('#head-id').html('')
            $('header').css('box-shadow' , '0px 0px 50px 1.5px #50d01d')
            $('.success').css('box-shadow' , '0px 0px 50px 1.5px #50d01d')
            $('.password-section').addClass("fold-up");
            $('.success').css("marginTop", 0);
            $('#head-id').html('')
            setTimeout(()=>{location.href = '/'} , 3000)
        }else {
            $('#head-id').html('The username or password is incorrect!')
            $("#head-id").css('color' , 'red')
        }
    })
}


