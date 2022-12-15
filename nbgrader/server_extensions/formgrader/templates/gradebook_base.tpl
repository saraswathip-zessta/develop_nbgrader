{%- extends 'base.tpl' -%} {%- block title -%}
<style>
    h1 {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
    }

    #exportButton {
        width: 9vw;
        border-radius: 2vw;
        border: none;
        margin-right: -19vw;
        background-color: #d2edfb;
        font-size: 1vw;
        font-weight: 100;
        padding: 0.5vw 1vw 0.5vw 1vw;
    }

    @media (max-width: 1440px) {
        #exportButton {
            width: 10vw;
            height: 5vh;
            font-size: 1.2vw;
        }

    }
</style>
Manual Grading
<button id="exportButton" onclick="exportData()">Export Grades</button>
{%- endblock -%} {%- block sidebar -%}
<li role="presentation">
    <a href="{{ base_url }}/formgrader/manage_assignments"><svg width="20" height="17" viewBox="0 0 20 22" fill="none"
            xmlns="http://www.w3.org/2000/svg">
            <path
                d="M3.24796 20.4734C2.95681 21.2609 2.01306 21.6828 1.13963 21.425C0.266502 21.1625 -0.205477 20.3094 0.0856168 19.5266L6.75004 1.52563C7.04171 0.740007 7.98963 0.314851 8.85942 0.576882C9.73442 0.838913 10.2032 1.68829 9.91671 2.47438L3.24796 20.4734ZM13.6094 0.520632C14.5157 0.656569 15.1303 1.42954 14.9792 2.24657L11.6459 20.2484C11.4948 21.0641 10.6355 21.6172 9.724 21.4813C8.81775 21.3453 8.20317 20.5719 8.35421 19.7516L11.6875 1.75344C11.8386 0.936413 12.698 0.384225 13.6094 0.520632ZM18.3334 0.500007C19.2553 0.500007 20 1.17173 20 2.00001V20C20 20.8297 19.2553 21.5 18.3334 21.5C17.4115 21.5 16.6667 20.8297 16.6667 20V2.00001C16.6667 1.17173 17.4115 0.500007 18.3334 0.500007Z"
                fill="white" />
        </svg>Manage Assignments</a>
</li>
<li role="presentation" class="active">
    <a href="{{ base_url }}/formgrader/gradebook">
        <svg width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path
                d="M0.566037 5.85703C0.450021 6.15938 0.548458 6.50039 0.787521 6.72187L2.30979 8.10703C2.27111 8.39883 2.25002 8.69766 2.25002 9C2.25002 9.30234 2.27111 9.60117 2.30979 9.89297L0.787521 11.2781C0.548458 11.4996 0.450021 11.8406 0.566037 12.143C0.720724 12.5613 0.907052 12.9656 1.11799 13.3488L1.28322 13.6336C1.51526 14.0203 1.77541 14.3859 2.06018 14.734C2.27111 14.9836 2.61213 15.0715 2.92151 14.973L4.87971 14.3473C5.3508 14.7094 5.90275 15.0117 6.42658 15.2438L6.86604 17.2512C6.93635 17.5676 7.18244 17.7926 7.50588 17.877C7.99104 17.9578 8.49025 18 9.03166 18C9.50978 18 10.009 17.9578 10.4942 17.877C10.8176 17.7926 11.0637 17.5676 11.134 17.2512L11.5735 15.2438C12.1289 15.0117 12.6492 14.7094 13.1203 14.3473L15.0771 14.973C15.3879 15.0715 15.7307 14.9836 15.9388 14.734C16.2239 14.3859 16.4841 14.0203 16.7161 13.6336L16.8806 13.3488C17.094 12.9656 17.2797 12.5613 17.4354 12.143C17.5493 11.8406 17.4533 11.4996 17.2122 11.2781L15.6913 9.89297C15.73 9.60117 15.75 9.30234 15.75 9C15.75 8.69766 15.73 8.39883 15.6913 8.10703L17.2122 6.72187C17.4533 6.50039 17.5493 6.16289 17.4354 5.85703C17.2797 5.43867 17.0937 5.03438 16.8806 4.65117L16.7165 4.36641C16.4841 3.97969 16.2239 3.61406 15.9388 3.26777C15.7307 3.01641 15.3879 2.92922 15.0771 3.02836L13.1203 3.65273C12.6492 3.28922 12.1289 2.98688 11.5735 2.7573L11.134 0.749883C11.0637 0.430664 10.8176 0.177187 10.4942 0.123398C10.009 0.0422227 9.50979 0 9.00002 0C8.49025 0 7.99104 0.0422227 7.50588 0.123398C7.18244 0.177187 6.93635 0.430664 6.86604 0.749883L6.42658 2.7573C5.90275 2.98688 5.3508 3.28922 4.87971 3.65273L2.92151 3.02836C2.61213 2.92922 2.27111 3.01641 2.06018 3.26777C1.77541 3.61406 1.51526 3.97969 1.28322 4.36641L1.11799 4.65117C0.907052 5.03438 0.720724 5.43867 0.566037 5.85703ZM9.00002 11.8125C7.44611 11.8125 6.18752 10.5539 6.18752 8.96836C6.18752 7.44609 7.44611 6.15586 9.00002 6.15586C10.5539 6.15586 11.8125 7.44609 11.8125 8.96836C11.8125 10.5539 10.5539 11.8125 9.00002 11.8125Z"
                fill="white" />
        </svg>Manual Grading</a>
</li>
{%- endblock -%} {%- block script -%}
<script>
    function exportData() {
        $.ajax({
            url: "api/customexport",
        }).done(function (res) {
            console.log(res);
            const response = JSON.parse(res);
            if (response.length > 0) {
                const dictionaryKeys = Object.keys(response[0]);
                const dictValuesAsCsv = response.map((dict) =>
                    dictionaryKeys.map((key) => dict[key]).join(",")
                );
                const result = [dictionaryKeys.join(","), ...dictValuesAsCsv].join("\n");
                var today = new Date();
                const dd = String(today.getDate()).padStart(2, "0");
                const mm = String(today.getMonth() + 1).padStart(2, "0");
                const yyyy = today.getFullYear();
                today = mm + "/" + dd + "/" + yyyy;
                const downloadLink = document.createElement("a");
                const blob = new Blob(["\ufeff", result]);
                const url = URL.createObjectURL(blob);
                downloadLink.href = url;
                downloadLink.download = "data_" + today + ".csv";
                document.body.appendChild(downloadLink);
                downloadLink.click();
                document.body.removeChild(downloadLink);
            }
            else {
                alert("No data to export")
            }
        });
    }
</script>

{%- endblock -%}
