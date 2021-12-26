// 폼(form)데이터 유효성 검증
async function FormValidation(){
    $("#form_data").validate({
        rules:{
            이름      :{required:true,rangelength:[2,999]},
            사번      :{required:true,rangelength:[2,999]},
            비밀번호  :{required:true,rangelength:[5,999]},
            이메일    :{required:true,email:true},
            소속본부  :{required:true,selectcheck: true},
            소속센터  :{required:true,selectcheck: true},
        },
        messages:{
            이름:{
                required:"이름은 필수 입력 항목입니다.",
                rangelength:"이름은 최소{0}글자 이상 작성해야합니다."
            },
            사번:{
                required:"사번은 필수 입력 항목입니다.",
                rangelength:"사번은 최소{0}글자 이상 작성해야합니다."
            },
            비밀번호:{
                required:"비밀번호는 필수 입력 항목입니다.",
                rangelength:"비밀번호는 최소{0}글자 이상 작성해야합니다."
            },
            이메일:{
                required:"이메일은 필수 입력 항목입니다.",
                email:"이메일 형식을 확인하세요."
            },
            소속본부:{
                required:"소속본부는 필수 선택 항목입니다.",
            },
            소속센터:{
                required:"소속센터는 필수 선택 항목입니다.",
            }
        },
    })
    jQuery.validator.addMethod('selectcheck', function (value) {
        return (value != '0');
    }, "year required");
};

//리포트 테이블  API 호출 및 랜더링
async function GetDiv1(){
    //Api Url 연결
    var api_url = '/APIAuthentication/Regist/GetDivList/';
    var base_url = window.location.origin;
    var call_url = base_url+api_url;
    $.ajax({
        url : call_url,
        type : "POST",
        contentType: "application/x-www-form-urlencoded; charset=UTF-8",
        dataType:'json',
        data : {
            "div1"  : "",
            "div2"  : "",
            "col"   : "1"
        },
        success : function(data){ // 수신 성공
            var results = data.data;
            var length = data.Count; // 수신된 데이터 갯수
            var str = '<option></option>';
            //var test = JSON.stringify(results[0].div1)
            for (let i=0; i<length; i++){
                str += "<option>"
                str += results[i].div1
                str += "</option>"
            }
            $("#div1").empty();
            $("#div1").append(str);
        },

        error : function(){
            alert("error");
        }
    });
};

//리포트 테이블  API 호출 및 랜더링
async function GetDiv2(div1){
    //Api Url 연결
    var api_url = '/APIAuthentication/Regist/GetDivList/';
    var base_url = window.location.origin;
    var call_url = base_url+api_url;
    $.ajax({
        url : call_url,
        type : "POST",
        contentType: "application/x-www-form-urlencoded; charset=UTF-8",
        dataType:'json',
        data : {
            "div1"  : div1,
            "div2"  : "",
            "col"   : "2"
        },
        success : function(data){ // 수신 성공
            var results = data.data;
            var length = data.Count; // 수신된 데이터 갯수
            var str = '';
            //var test = JSON.stringify(results[0].div1)
            for (let i=0; i<length; i++){
                str += "<option>"
                str += results[i].div2
                str += "</option>"
            }
            $("#div2").empty();
            $("#div2").append(str);
            
        },

        error : function(){
            alert("error");
        }
    });
};