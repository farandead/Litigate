function typeEffect(element, text, speed, callback) {
    element.innerHTML = "";
    let i = 0;
    let timer = setInterval(function() {
        if (i < text.length) {
            element.append(text.charAt(i));
            i++;
        } else {
            clearInterval(timer);
            callback(); // Callback when typing is done
        }
    }, speed);
}
const textContent = {
    "Lease Clarity": "Review lease terms for rent, maintenance, and exit conditions.",
    "Maintenance Reports": "Document and report issues promptly to your landlord.",
    "Deposit Rules": "Understand conditions for security deposit return.",
    "Rent Increase Negotiation": "Check lease and laws before negotiating rent changes.",
    "Noise Issue Handling": "Address neighbor noise first, then escalate to landlord if needed.",
    "Lease Renewal Strategy": "Assess and negotiate lease terms upon renewal.",
    "Rent Payment Terms": "Understand due dates, methods, and late fee policies for rent payments.",
    "Property Inspection Tips": "Document property condition at move-in and move-out to avoid disputes.",
    "Handling Lease Violations": "Know your rights and responsibilities in case of lease violations.",
    "Subletting Procedures": "Check lease terms and local laws before subletting your rental unit.",
    "Eviction Process Understanding": "Be aware of legal eviction procedures and tenant rights during the process.",
    "Emergency Repairs Knowledge": "Learn about handling emergency repairs and landlord's responsibilities.",
    "Tenant Privacy Rights": "Know your rights regarding landlord entry and privacy.",
    "Pet Policy Clarification": "Understand the rules and conditions for keeping pets in the rental property."

    // ... Add more pairs
};
function animateText(keys, index) {
    if (index < keys.length) {
        let heading = document.getElementById('animated-heading');
        let paragraph = document.getElementById('animated-paragraph');
        let currentKey = keys[index];

        typeEffect(heading, currentKey, 100, () => {
            typeEffect(paragraph, textContent[currentKey], 50, () => {
                // Wait for some time before moving to the next pair
                setTimeout(() => {
                    animateText(keys, index + 1);
                }, 3000); // Adjust the delay as needed
            });
        });
    }
}
// Initial typing effect on load
window.onload = function() {
    let keys = Object.keys(textContent);
    animateText(keys, 0);
};