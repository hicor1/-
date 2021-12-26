
//리포트 테이블  API 호출 및 랜더링
async function ReportView(div_list_id, Year, WeekNum){
    //Api Url 연결
    var api_url = '/APIreport/ReportView/ReportView/';
    var base_url = window.location.origin;
    var call_url = base_url+api_url;
    $.ajax({
        url : call_url,
        type : "GET",
        contentType: "application/x-www-form-urlencoded; charset=UTF-8",
        dataType:'json',
        data : {
            "div_list_id" : div_list_id,
            "Year"        : Year,
            "WeekNum"     : WeekNum
        },
        success : function(data){ // 수신 성공
            var results = data.data;
            var RegisterdedPerson = data.RegisterdedPerson; // 수신된 데이터 갯수
            var length = data.Count; // 수신된 데이터 갯수

            $("#reportbody").empty();
            $("#reportbody").append(results);

            //// 등록 또는 미등록 회원 표기하기 ////
            //.1 실적-등록완료
            var string = ""
            var 실적_등록 = RegisterdedPerson.실적_등록
            for (let i=0; i<실적_등록.length; i++){
                string += '<div style="float: left; margin-right: 10px;" class="form-check form-check-success"><input class="form-check-input" type="radio" name="" id="Success" checked=""><label class="form-check-label" for="Success">'
                string += 실적_등록[i]
                string += '</label></div>'
            }
            $("#실적_등록").empty();
            $("#실적_등록").append(string);

            //.2 실적-미등록
            var string = ""
            var 실적_미등록 = RegisterdedPerson.실적_미등록
            for (let i=0; i<실적_미등록.length; i++){
                string += '<div style="float: left; margin-right: 10px;" class="form-check form-check-danger"><input class="form-check-input" type="radio" name="" id="Success" checked=""><label class="form-check-label" for="Success">'
                string += 실적_미등록[i]
                string += '</label></div>'
            }
            $("#실적_미등록").empty();
            $("#실적_미등록").append(string);

            //.3 계획-등록완료
            var string = ""
            var 계획_등록 = RegisterdedPerson.계획_등록
            for (let i=0; i<계획_등록.length; i++){
                string += '<div style="float: left; margin-right: 10px;" class="form-check form-check-success"><input class="form-check-input" type="radio" name="" id="Success" checked=""><label class="form-check-label" for="Success">'
                string += 계획_등록[i]
                string += '</label></div>'
            }
            $("#계획_등록").empty();
            $("#계획_등록").append(string);

            //.4 계획-미등록
            var string = ""
            var 계획_미등록 = RegisterdedPerson.계획_미등록
            for (let i=0; i<계획_미등록.length; i++){
                string += '<div style="float: left; margin-right: 10px;" class="form-check form-check-danger"><input class="form-check-input" type="radio" name="" id="Success" checked=""><label class="form-check-label" for="Success">'
                string += 계획_미등록[i]
                string += '</label></div>'
            }
            $("#계획_미등록").empty();
            $("#계획_미등록").append(string);

            
        },

        error : function(){
            alert("error");
        }
    });
};


//본부 > (나의) 부서 리스트 리턴
async function MyDivList(div1, div2){
    //Api Url 연결
    var api_url = '/APIreport/ReportView/GetDivList/';
    var base_url = window.location.origin;
    var call_url = base_url+api_url;
    $.ajax({
        url : call_url,
        type : "GET",
        contentType: "application/x-www-form-urlencoded; charset=UTF-8",
        dataType:'json',
        data : {
            "div1" : div1,
            "div2" : div2,
        },
        success : function(data){ // 수신 성공
            var results = data.data;
            var length = data.Count; // 수신된 데이터 갯수

            $("#MyDivList").empty();
            $("#MyDivList").append(results);
            
        },

        error : function(){
            alert("error");
        }
    });
};

//본부 > (전체) 부서 리스트 리턴
async function GetDivList(div1, div2){
    //Api Url 연결
    var api_url = '/APIreport/ReportView/GetDivList/';
    var base_url = window.location.origin;
    var call_url = base_url+api_url;
    $.ajax({
        url : call_url,
        type : "GET",
        contentType: "application/x-www-form-urlencoded; charset=UTF-8",
        dataType:'json',
        data : {
            "div1" : div1,
            "div2" : div2,
        },
        success : function(data){ // 수신 성공
            var results = data.data;
            var length = data.Count; // 수신된 데이터 갯수

            $("#DivList").empty();
            $("#DivList").append(results);
            
        },

        error : function(){
            alert("error");
        }
    });
};

//업무보고 작성을 위한 modal창 띄우기
async function Modalshow(Isshow){

    if (Isshow === true) {
        $("#inlineForm").addClass("show");
        $("#inlineForm").css("display","block");
        $("#fade").addClass("modal-backdrop fade show");
    } else {
        $("#inlineForm").removeClass("show");
        $("#inlineForm").css("display","none");
        $("#fade").removeClass("modal-backdrop fade show");
    }
};

// 팝업Modal창을 띄우는 이벤트 ( onClick으로 할당 )
async function Popmodal(sep1, sep2, sep3, sep4, TemplateName, Year, WeekNum, id,  Div){
    // 구분 정보 받아오기
   //(참고) var 전략방향 = ClickedTechTd.parents("tr").children("th")[0].textContent;
    var str = sep1 + " > " + sep2 + " > " + sep3 + " > " + sep4
    //구분 정보로 부터 분류 만들기
    $("#sep").empty();
    $("#sep").append(str);
    //hidden 데이터 입히기
    $("#TemplateName").attr("value", TemplateName)
    $("#ContentsID")  .attr("value", id)
    $("#Div")         .attr("value", Div)
    $("#등록일시")     .attr("value", "TempData") // (임시데이터 삽입,)백앤드 서버에서 등록일시 입력

    //신규등록이므로, 등록버튼은보이고, 삭제&수정버튼은 감춘다
    $('#ReportRegist').removeClass('hidden');
    $('#ReportDelete').addClass('hidden');
    $('#ReportModify').addClass('hidden');

    //form 비우기
    $('#form_data')[0].reset();

    //모달창 띄우기
    Modalshow(Isshow = true);

    }

// 데이터 피커 Function ( 이벤트 등록 )
async function Datepicker(){
    //https://kkyunstory.tistory.com/128
    $('.input-group.date').datepicker({
        calendarWeeks: false,
        todayHighlight: true,
        autoclose: true,
        format: "yyyy-mm-dd",
        language: "kr"
    });
}

// Form에서 시작일이 변경되면 종료일 변경되는 이벤트  
async function change_date(){
    //https://kkyunstory.tistory.com/128
    $("#시작일").change(function(){
    //날짜 입히기
    var start_date = $("#시작일").val();
    $("#종료일").val(start_date)
    });

}

// 폼(form)데이터 유효성 검증 & 데이터 저장 ( 등록, 삭제, 수정 )
async function get_form_data(){
    //https://blog.kingbbode.com/28
    //https://goodteacher.tistory.com/162
        //필수항목(required)검사
    $("#form_data").validate({
        rules:{
            제목:{required:true,rangelength:[2,999]},
            내용:{required:true,rangelength:[5,999]},
            담당자:{required:true,rangelength:[2,999]},
            시작일:{required:true, date:true},
            종료일:{required:true, date:true},
            email:{email:true}
        },
        messages:{
            제목:{
                required:"제목은 필수 입력 항목입니다.",
                rangelength:"제목은 최소{0}글자 이상 작성해야합니다."
            },
            내용:{
                required:"내용은 필수 입력 항목입니다.",
                rangelength:"내용은 최소{0}글자 이상 작성해야합니다."
            },
            담당자:{
                required:"담당자는 필수 입력 항목입니다.",
                rangelength:"담당자는 최소{0}글자 이상 작성해야합니다."
            },
            시작일:{
                required:"시작일은 필수 입력 항목입니다.",
                //date:"날짜형식을 확인해주세요"
            },
            종료일:{
                required:"종료일은 필수 입력 항목입니다.",
                //date:"날짜형식을 확인해주세요"
            },
            email:{
                email:"이메일 형식을 확인하세요."
            }
        },
    })
};

/// 폼(form)에 있는 3개버튼 ( 등록 / 수정 / 삭제 )버튼에 대한 기능 정의
async function ReportSubmitAction(){
    //1. [등록]
    $("#ReportRegist").click(function(){
        // 폼(form)이 유효하다면,
        if ($('#form_data').valid()){
            //0. 해당 내용으로 등록할지 결정 문의
            if (!confirm("해당 내용으로 등록하시겠습니까?")) {
                // 취소(아니오) 버튼 클릭 시 이벤트
                alert("등록이 취소되었습니다.");
            } else {
                // 확인(예) 버튼 클릭 시 이벤트
                // (업무정보)데이터 모으기 
                var formdata = {};
                $.each($('#form_data').serializeArray(), function() {
                    formdata[this.name] = this.value;
                });
                //( 그외 정보:템플릿이름, id, 주차, 실적  or 계획 )데이터 모으기
                //formdata.push({name: 'templatename', value: $("#form_data")});
                
                // 데이터 등록
                FormDataRegist(formdata);
                // 안내
                alert("성공적으로 등록이 완료되었습니다.");
                // 리포트 다시 뿌려주기
                ReportView(
                    div_list_id = $('#div_list_id').val(), 
                    Year        = $('#Year').val(),
                    WeekNum     = $('#WeekNum').val(),
                    )
            }
            // 창닫기
            Modalshow(Isshow = false)
        }else{
            //폼이 유효하지 않은 경우
        }
    });
    //2. [삭제]
    $("#ReportDelete").click(function(){
        // 폼(form)이 유효하다면,
        if ($('#form_data').valid()){
            //0. 해당 내용으로 등록할지 결정 문의
            if (!confirm("해당 내용을 삭제하시겠습니까?")) {
                // 취소(아니오) 버튼 클릭 시 이벤트
                alert("삭제가 취소되었습니다.");
            } else {
                // 데이터 삭제
                FormDataDelete(ReportID = $('#ReportID').attr('value'));
                // 안내
                alert("성공적으로 삭제가 완료되었습니다.");
                // 리포트 다시 뿌려주기
                ReportView(
                    div_list_id = $('#div_list_id').val(), 
                    Year        = $('#Year').val(),
                    WeekNum     = $('#WeekNum').val(),
                    )
            }
            // 창닫기
            Modalshow(Isshow = false)
        }else{
            //폼이 유효하지 않은 경우
        }
    });
    //3. [수정]
    $("#ReportModify").click(function(){
        // 폼(form)이 유효하다면,
        if ($('#form_data').valid()){
            //0. 해당 내용으로 등록할지 결정 문의
            if (!confirm("해당 내용으로 수정하시겠습니까?")) {
                // 취소(아니오) 버튼 클릭 시 이벤트
                alert("수정이 취소되었습니다.");
            } else {
                // 확인(예) 버튼 클릭 시 이벤트
                // (업무정보)데이터 모으기 
                var formdata = {};
                $.each($('#form_data').serializeArray(), function() {
                    formdata[this.name] = this.value;
                });
                //( 그외 정보:템플릿이름, id, 주차, 실적  or 계획 )데이터 모으기
                //formdata.push({name: 'templatename', value: $("#form_data")});
                
                // 데이터 등록
                FormDataModify(formdata);
                // 안내
                alert("성공적으로 수정이 완료되었습니다.");
                // 리포트 다시 뿌려주기
                ReportView(
                    div_list_id = $('#div_list_id').val(), 
                    Year        = $('#Year').val(),
                    WeekNum     = $('#WeekNum').val(),
                    )
            }
            // 창닫기
            Modalshow(Isshow = false)
        }else{
            //폼이 유효하지 않은 경우
        }
    });
};

//주간업무보고 (폼데이터) 등록
async function FormDataRegist(formdata){
    //Api Url 연결
    var api_url = '/APIreport/ReportView/ReportRegist/';
    var base_url = window.location.origin;
    var call_url = base_url+api_url;

    $.ajax({
        url : call_url,
        type : "POST",
        dataType:'json',
        data : {
            'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),//html랜더링때 배포한 csrf토큰키 확인
            'formdata':JSON.stringify(formdata),
        },
        success : function(data){ 
            // 수신 성공
        },

        error : function(){
            // 수신 에러
            alert("error");
        }
    });
};

//주간업무보고 (폼데이터) 삭제
async function FormDataDelete(ReportID){
    //Api Url 연결
    var api_url = '/APIreport/ReportView/ReportDelete/';
    var base_url = window.location.origin;
    var call_url = base_url+api_url;

    $.ajax({
        url : call_url,
        type : "POST",
        dataType:'json',
        data : {
            'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),//html랜더링때 배포한 csrf토큰키 확인
            'ReportID':ReportID,
        },
        success : function(data){ 
            // 수신 성공
        },

        error : function(){
            // 수신 에러
            alert("error");
        }
    });
};

//주간업무보고 (폼데이터) 수정
async function FormDataModify(formdata){
    //Api Url 연결
    var api_url = '/APIreport/ReportView/ReportModify/';
    var base_url = window.location.origin;
    var call_url = base_url+api_url;

    $.ajax({
        url : call_url,
        type : "POST",
        dataType:'json',
        data : {
            'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),//html랜더링때 배포한 csrf토큰키 확인
            'formdata':JSON.stringify(formdata),
        },
        success : function(data){ 
            // 수신 성공
        },

        error : function(){
            // 수신 에러
            alert("error");
        }
    });
};

//주차(WeekNum) 만들기
async function GetWeekHtml(Year,WeekNum,div_list_id,div1,div2){
    //(참고)href="/report/report_main/{Year}/{WeekNum}/{div_list_id}/{div1}/{div2}
    // 오늘에 해당하는 주차 구하기
    var NowWeekNum = new Date().getWeek();
    // 선택된 주차 구하기
    var SelectedWeekNum = WeekNum;
    var str = '';
    for (let i=0; i<=NowWeekNum; i++) {
        if (i == SelectedWeekNum){ // 선택된 주차에 해당하는 주는 활성화(active)한다.
            str +='<a class="dropdown-item active" ';
        }else{
            str +='<a class="dropdown-item" ';
        }
        str +='href="/report/report_main/'
        str +=Year + "/" + i + "/" + div_list_id + "/" + div1 + "/" + div2;
        str +='"';
        str +='>' + i + ' 주차</a>';
    }
    // 해당 id에 덮어써주기
    $("#GetWeekHtml").empty();
    $("#GetWeekHtml").append(str);

};

// 이번주가 몇주차(WeekNum)인지 확인하는 함수
Date.prototype.getWeek = function (dowOffset) {
    /*getWeek() was developed by Nick Baicoianu at MeanFreePath: http://www.meanfreepath.com */
  
    dowOffset = typeof(dowOffset) == 'number' ? dowOffset : 0; // dowOffset이 숫자면 넣고 아니면 0
    var newYear = new Date(this.getFullYear(),0,1);
    var day = newYear.getDay() - dowOffset; //the day of week the year begins on
    day = (day >= 0 ? day : day + 7);
    var daynum = Math.floor((this.getTime() - newYear.getTime() -
      (this.getTimezoneOffset()-newYear.getTimezoneOffset())*60000)/86400000) + 1;
    var weeknum;
    //if the year starts before the middle of a week
    if(day < 4) {
      weeknum = Math.floor((daynum+day-1)/7) + 1;
      if(weeknum > 52) {
        let nYear = new Date(this.getFullYear() + 1,0,1);
        let nday = nYear.getDay() - dowOffset;
        nday = nday >= 0 ? nday : nday + 7;
        /*if the next year starts before the middle of
          the week, it is week #1 of that year*/
        weeknum = nday < 4 ? 1 : 53;
      }
    }
    else {
      weeknum = Math.floor((daynum+day-1)/7);
    }
    return weeknum;
  };

// 해당주차에 대한 시작일과 종료일 구하기
//(참고)https://gist.github.com/Abhinav1217/5038863
function getDateRangeOfWeek(weekNo){
    var d1 = new Date();
    numOfdaysPastSinceLastMonday = eval(d1.getDay()- 1);
    d1.setDate(d1.getDate() - numOfdaysPastSinceLastMonday);
    var weekNoToday = d1.getWeek();
    var weeksInTheFuture = eval( weekNo - weekNoToday );
    d1.setDate(d1.getDate() + eval( 7 * weeksInTheFuture ));
    var rangeIsFrom = d1.getFullYear() + "." + eval(d1.getMonth()+1) + "." + d1.getDate() + "";
    d1.setDate(d1.getDate() + 4);
    var rangeIsTo   = d1.getFullYear() + "." + eval(d1.getMonth()+1) + "." + d1.getDate() + "";

    var FullDateText = "(" + rangeIsFrom + " ~ " + rangeIsTo + ")";

    return {
        start        : rangeIsFrom,
        end          : rangeIsTo,
        FullDateText : FullDateText
    };
}; 

// 주간업무보고 Detail 사항 보여주기
async function GetReportDetail(e, ReportID){ //this를 e로 받아온다

    // ReportID 정보를 서버로 보내서  form html 받아오기
    //Api Url 연결
    var api_url = '/APIreport/ReportView/GetReportDetail/';
    var base_url = window.location.origin;
    var call_url = base_url+api_url;

    $.ajax({
        url : call_url,
        type : "POST",
        dataType:'json',
        data : {
            'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),//html랜더링때 배포한 csrf토큰키 확인
            'ReportID'           : ReportID
        },
        success : function(data){ 
            // 팝업버튼 대신 눌러주기
            $(e).closest("td").find('span').trigger("click");
            // 수신 성공
            var results = data.data;
            var length = data.Count; // 수신된 데이터 갯수
            // form에 데이터 입히기
            $("#제목")      .val(results[0].제목);
            $("#내용")      .val(results[0].내용);
            $("#담당자")    .val(results[0].담당자);
            $("#장소업체")  .val(results[0].장소업체);
            $("#금액")      .val(results[0].금액);
            $("#단위")      .val(results[0].단위);
            $("#출장여부")  .val(results[0].출장여부);
            $("#중요도")    .val(results[0].중요도);
            $("#시작일")    .val(results[0].시작일);
            $("#종료일")    .val(results[0].종료일);
            //수정에 필요한 리포트 식별번호를 몰래 심어놓는다
            $("#ReportID")  .attr('value', results[0].id);
            
            //삭제&수정이므로, 등록버튼은 감추고, 삭제&수정버튼은 보인다.
            $('#ReportRegist').addClass('hidden');
            $('#ReportDelete').removeClass('hidden');
            $('#ReportModify').removeClass('hidden');
            
        },

        error : function(){
            // 수신 에러z
            alert("error");
        }
    });

}

//검색어("제목") 추천기능 Function
async function TitleRecommand(Query, ContentsID, div_list_id){
    //Api Url 연결
    var api_url = '/APIreport/ReportView/Title_Sim_Get/';
    var base_url = window.location.origin;
    var call_url = base_url+api_url;

    // 2글자 이상일때만 모듈 작동
    if (Query.length >= 2){

        $.ajax({
            url : call_url,
            type : "GET",
            dataType:'json',
            data : {
                'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),//html랜더링때 배포한 csrf토큰키 확인
                'Query'      :Query,
                'ContentsID' :ContentsID,
                'div_list_id':div_list_id,
            },
            success : function(data){ 
                // 수신 성공
                var string = "";
                var Title_list= data.data;
                var count = Title_list.length;
                // 추천결과가 1개 이상일 경우에만 리스트 리턴
                if (count >= 1){
                    for (let i=0; i<Title_list.length; i++){
                        string += "<option value="
                        string += '"' + Title_list[i] + '"' + '>'
                    }

                } else{
                    string += "<option value=" + '"' + "추천검색결과가 존재하지 않습니다." +'"'+ '>';
                }
                $("#title_list").empty();
                $("#title_list").append(string);
                //console.log(string);
            },

            error : function(){
                // 수신 에러
                //alert("error");
            }
        });
    } else {

    }
};