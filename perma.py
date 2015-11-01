import os
import os.path

import dill

def perma(unique=None, dir=None):
    def decorate(basetype):
        class Perma(basetype):

            _save_dir = os.path.expanduser(
                "%s/%s/%s" % (
                    dir or "~/.perma",
                    str(basetype.__module__), 
                    str(basetype.__name__)
                )
            )

            def __init__(self, *args, **kwargs):
                self._unique = unique
                if not os.path.isdir(Perma._save_dir):
                    os.makedirs(Perma._save_dir)
                super(Perma, self).__init__(*args, **kwargs)

            @classmethod
            def _save_file(cls, unique_id, mode):
                return open(os.path.abspath(
                    os.path.join(Perma._save_dir, unique_id)
                ), mode)

            def save(self):
                return dill.dump(self, Perma._save_file(self._unique, 'w'))

            @classmethod
            def load(cls, unique_id):
                return dill.load(Perma._save_file(unique_id, 'r'))

        # preserve metadata
        Perma.__module__ = basetype.__module__
        Perma.__name__ = basetype.__name__
        return Perma
    return decorate

if __name__ == "__main__":

    @perma(unique="name")
    class Dog(object):

        def __init__(self, name):
            self.name = name
            self.times_barked = 0

        def bark(self):
            self.times_barked += 1
            print("%s: bark!" % self.name)

    fido = Dog("fido")
    fido.bark()
    fido.save()
    print "Times barked: %d" % fido.times_barked
    del fido
    fido = Dog.load('fido')
    print "Times barked: %d" % fido.times_barked
