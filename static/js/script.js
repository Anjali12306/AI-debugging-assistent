document.addEventListener("DOMContentLoaded", () => {
    const textarea = document.getElementById("code");
    const form = document.getElementById("debug-form");
    const button = document.getElementById("analyze-button");
    const sampleButtons = document.querySelectorAll(".sample-button");
    const copyButton = document.querySelector(".copy-button");
    const languageSelect = document.getElementById("language");
    const samples = {
        Python: {
            syntax: "for i in range(5)\n    print(i)",
            type: 'num = 5\ntext = "10"\nprint(num + text)',
            logic: 'numbers = [10, 20, 30]\ntotal = 0\n\nfor n in numbers:\n    total += n\n\nprint("Average:", total)',
        },
        C: {
            syntax: '#include <stdio.h>\n\nint main() {\n    int i;\n    for(i = 0; i < 5; i++)\n        printf("%d\\n", i)\n    return 0;\n}',
            type: '#include <stdio.h>\n\nint main() {\n    int number = 5;\n    char text[] = "10";\n    printf("%d", number + text);\n    return 0;\n}',
            logic: '#include <stdio.h>\n\nint main() {\n    int numbers[] = {10, 20, 30};\n    int total = 0;\n    for (int i = 0; i < 3; i++) {\n        total += numbers[i];\n    }\n    printf("Average: %d", total);\n    return 0;\n}',
        },
        "C++": {
            syntax: '#include <iostream>\nusing namespace std;\n\nint main() {\n    for (int i = 0; i < 5; i++)\n        cout << i << endl\n    return 0;\n}',
            type: '#include <iostream>\nusing namespace std;\n\nint main() {\n    int num = 5;\n    string text = "10";\n    cout << num + text;\n    return 0;\n}',
            logic: '#include <iostream>\nusing namespace std;\n\nint main() {\n    int values[] = {10, 20, 30};\n    int total = 0;\n    for (int i = 0; i < 3; i++) {\n        total += values[i];\n    }\n    cout << "Average: " << total;\n    return 0;\n}',
        },
        Java: {
            syntax: 'public class Main {\n    public static void main(String[] args) {\n        for (int i = 0; i < 5; i++)\n            System.out.println(i)\n    }\n}',
            type: 'public class Main {\n    public static void main(String[] args) {\n        int num = 5;\n        String text = "10";\n        System.out.println(num + text.charAt(0));\n    }\n}',
            logic: 'public class Main {\n    public static void main(String[] args) {\n        int[] numbers = {10, 20, 30};\n        int total = 0;\n        for (int n : numbers) {\n            total += n;\n        }\n        System.out.println("Average: " + total);\n    }\n}',
        },
        JavaScript: {
            syntax: 'for (let i = 0; i < 5; i++) {\n    console.log(i)\n',
            type: 'let num = 5;\nlet text = "10";\nconsole.log(num + text.toFixed(2));',
            logic: 'const numbers = [10, 20, 30];\nlet total = 0;\nfor (const n of numbers) {\n    total += n;\n}\nconsole.log("Average:", total);',
        },
    };

    if (textarea && !textarea.value.trim()) {
        textarea.focus();
    }

    if (form && button) {
        form.addEventListener("submit", () => {
            document.body.classList.add("is-submitting");
            button.disabled = true;
        });
    }

    sampleButtons.forEach((sampleButton) => {
        sampleButton.addEventListener("click", () => {
            const sampleKey = sampleButton.dataset.sample;
            const selectedLanguage = languageSelect ? languageSelect.value : "Python";
            const languageSamples = samples[selectedLanguage] || samples.Python;
            if (textarea && sampleKey && languageSamples[sampleKey]) {
                textarea.value = languageSamples[sampleKey];
                textarea.focus();
            }
        });
    });

    if (copyButton) {
        copyButton.addEventListener("click", async () => {
            const targetId = copyButton.dataset.copyTarget;
            const target = targetId ? document.getElementById(targetId) : null;
            if (!target) {
                return;
            }

            try {
                await navigator.clipboard.writeText(target.textContent || "");
                copyButton.textContent = "Copied";
                setTimeout(() => {
                    copyButton.textContent = "Copy";
                }, 1400);
            } catch {
                copyButton.textContent = "Unavailable";
            }
        });
    }
});
