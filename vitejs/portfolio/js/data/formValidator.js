import htmx from 'htmx.org';
export default (criteria) => ({
  formData: {},
  errors: {},

  // Initialize formData based on criteria keys and attach blur event listeners
  init() {
    Object.keys(criteria).forEach((fieldName) => {
      this.formData[fieldName] = '';
      // Select the field using its name attribute
      const fieldElement = document.querySelector(`[name="${fieldName}"]`);
      if (fieldElement) {
        // Attach a blur event listener to the field
        fieldElement.addEventListener('blur', () => {
          this.validateField(fieldName, criteria[fieldName]);
        });
      }
    });
  },

  validateForm() {
    let isValid = true;
    Object.keys(criteria).forEach((field) => {
      const fieldIsValid = this.validateField(field, criteria[field]);
      if (!fieldIsValid) isValid = false;
    });

    if (isValid) {
      console.log('Form is valid, proceed with submission.');
      // return true;

      const form = this.$refs.form; // Assuming you've set x-ref="form" on your form element
      // // Programmatically set HTMX attributes if they're not statically set in HTML
      // form.setAttribute('hx-post', form.action); // or a specific URL if needed
      // form.setAttribute('hx-target', '#main-section');

      // // Use HTMX to trigger the form submission
      // htmx.trigger(form, 'submit', { target: form });

      // const form = document.getElementById('signup-form'); // Replace 'myForm' with your actual form ID or use a different selector if needed
      // Set HTMX attributes for AJAX submission
      // form.setAttribute('hx-post', 'URL_TO_SUBMIT_FORM'); // Replace URL_TO_SUBMIT_FORM with the actual URL where the form should be submitted
      // form.setAttribute('hx-target', '#main-content'); // The target where the response will be loaded
      // form.setAttribute('hx-include', '*'); // Optional: Include all form fields in the submission
      // You can add more HTMX attributes as needed, for example, to handle responses

      // Programmatically trigger the form submission via HTMX
      // form.dispatchEvent(new CustomEvent('submit-form', { bubbles: true, cancelable: true }));

      // const form = document.getElementById('signup-form');
      // const htmxEvent = new CustomEvent('submit-form', { bubbles: true, cancelable: true });
      // form.dispatchEvent(htmxEvent);
      // form.submit();
      // this.$refs.form.requestSubmit();

      console.log(form);

      // // Directly trigger the HTMX request
      // htmx.ajax('POST', form.action, form, {
      //   target: '#main-section',
      // });
    } else {
      console.log('Form is invalid, please correct the errors.');
      return false;
    }
  },

  validateField(field, rules) {
    let fieldIsValid = true;
    this.errors[field] = null; // Reset any previous error for the field

    for (const rule of rules) {
      for (const [ruleKey, ruleDetails] of Object.entries(rule)) {
        if (ruleKey !== 'message') {
          const validatorFunction = this[ruleKey];
          const validationArguments = Array.isArray(ruleDetails) ? ruleDetails : [ruleDetails];
          if (typeof validatorFunction === 'function') {
            if (!validatorFunction.call(this, this.formData[field], ...validationArguments)) {
              // Replace placeholders in the message
              let message = rule.message;
              validationArguments.forEach((arg, index) => {
                message = message.replace(new RegExp(`\\{${index}\\}`, 'g'), arg);
              });
              this.errors[field] = message;
              fieldIsValid = false;
              break; // Stop checking further rules for this field
            }
          } else {
            console.error(`Validator function for "${ruleKey}" is not defined.`);
          }
        }
      }
      if (!fieldIsValid) break; // If validation failed, stop processing other rules
    }

    return fieldIsValid;
  },

  // Validation Rule Helpers
  required(value) {
    return value !== undefined && value !== null && value.length > 0;
  },
  email(value) {
    return /^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/.test(
      value
    );
  },
  maxLength(value, max) {
    return value.length <= max;
  },
  equalTo(value, otherValue) {
    return value === this.formData[otherValue];
  },
  range(value, min, max) {
    return value >= min && value <= max;
  },
});
