from rest_framework.serializers import ValidationError


class IO():
    def _error(self, message):
        raise ValidationError({
            'error':{
                'detail': message
            }
        })

    def _success(self, message): 
        return {
            'success' :{
                'detail': message
            }
        }

io = IO()