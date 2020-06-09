import { extend } from 'vee-validate';
import { required, email, min } from 'vee-validate/dist/rules';

extend('required', {
    ...required,
    message: 'Este campo es requerido'
  });

extend('email', {
    ...email,
    message: 'No es un correo válido'
});

extend('min', {
    ...min,
    message: 'Debe tener un mínimo de {length} caracteres'
});


