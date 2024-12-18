export class Model {


  constructor() { }

}


export class UserForRegister {
  constructor(email: string, firstname: string, lastname: string, password: string, birthday: string) {

    this.email = email;
    this.firstName = firstname;
    this.lastName = lastname;
    this.birthday = birthday;
    this.password = password;

}
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  birthday: string;


}


