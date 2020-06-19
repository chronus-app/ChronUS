import { extend } from 'vee-validate';
import { required, email, regex, min } from 'vee-validate/dist/rules';

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

extend('date_gte', { 
    validate: date => {
        let today = new Date().setHours(0,0,0,0);
        let receivedDate = new Date(date).setHours(0,0,0,0);
        return receivedDate >= today;
    },
    message: 'La fecha debe ser igual o mayor que la fecha actual'
});

extend('regex', {
    ...regex,
    message: 'Debe tener el formato hh:mm'
});

extend('min_time', { 
    validate: time => {
        let splittedTime = time.split(':');
        let hours = splittedTime[0];
        let minutes = splittedTime[1];

        let receivedDate =  new Date();
        receivedDate.setHours(hours, minutes, 0, 0);

        let minDate = new Date();
        minDate.setHours(0, 15, 0, 0);
        
        return receivedDate >= minDate;
    },
    message: 'El mínimo son 15 minutos'
});

extend('val_minutes', { 
    validate: time => {
        let splittedTime = time.split(':');
        let minutes = splittedTime[1];

        minutes = minutes == '0' ? '00' : minutes;
    
        let allowedMinutes = ['00', '15', '30', '45'];
        
        return allowedMinutes.includes(minutes);
    },
    message: 'Los minutos deben ser 15, 30 o 45'
});


