import { AbstractControl, ValidationErrors } from "@angular/forms";

export class PasswordValidator
{
    static passwordMatchValidator(control: AbstractControl) {
        const password: string = control.value.get('password').value; // get password from our password form control
        const confirmPassword: string = control.value.get('confirmPassword').value; // get password from our confirmPassword form control
        // compare is the password math
        if (password !== confirmPassword) {
          // if they don't match, set an error in our confirmPassword form control
          control.value.get('confirmPassword').setErrors({ NoPassswordMatch: true });
        }
      }
}