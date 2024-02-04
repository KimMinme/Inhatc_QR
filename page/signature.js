const canvas = document.getElementById('signature_pad');
const signaturePad = new SignaturePad(canvas);
document.getElementById('clear').addEventListener('click', () => {
    signaturePad.clear();
});

document.getElementById('submit_button').addEventListener('click', async () => {
    const willSubmit = confirm("제출하시겠습니까?");
    if (willSubmit == false) return;

    const student_id = document.getElementById('student_id').value;
    const student_name = document.getElementById('student_name').value;
    const student_phone_number = document.getElementById('student_phone_number').value;
    const URL = signaturePad.toDataURL();
    const json = {
        studentId: student_id,
        studentName: student_name,
        studentPhoneNumber: student_phone_number,
        URL: URL
    }
    await axios.post('http://jwjung.kro.kr:80/register', json);

    alert("제출되었습니다.");
    document.querySelector('form').reset();
    signaturePad.clear();
});