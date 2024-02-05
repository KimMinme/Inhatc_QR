const canvas = document.getElementById('signature_pad');
const signaturePad = new SignaturePad(canvas);
document.getElementById('clear').addEventListener('click', () => {
    signaturePad.clear();
});

document.getElementById('submit_button').addEventListener('click', async () => {
    const student_id = document.getElementById('student_id').value;
    if (student_id.length != 9) {
        alert("학번이 유효하지 않습니다.");
        return;
    }
    const student_phone_number = document.getElementById('student_phone_number').value;
    if (student_phone_number.length != 11) {
        alert("전화번호가 유효하지 않습니다.");
        return;
    }
    if (signaturePad.isEmpty()) {
        alert("서명해 주십시오.");
        return;
    }
    const willSubmit = confirm("제출하시겠습니까?");
    if (willSubmit == false) return;

    const student_name = document.getElementById('student_name').value;
    const URL = signaturePad.toDataURL();
    const json = {
        studentId: student_id,
        studentName: student_name,
        studentPhoneNumber: student_phone_number,
        URL: URL
    }
    const response = await axios.post('http://jwjung.kro.kr:20000/register', json);
    if (!response.isIn) {
        alert("졸업자 명단에 없는 학번과 이름입니다.");
        return;
    }

    alert("제출되었습니다.");
    document.querySelector('form').reset();
    signaturePad.clear();
});