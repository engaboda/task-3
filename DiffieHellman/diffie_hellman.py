from collections import Counter
import utils


class DiffieHellman:
    """
        private=XA,
        generator=alpha
        prime=q
    """

    @property
    def generte_private_key(self, length=3):
        """
            equla XA in the diagram
        """
        return utils.generate_number(length)

    @property
    def generte_generator(self, length=3):
        """
            equal Alpha in the diagram
            should be prime
        """
        return utils.generate_number(length)

    @property
    def generte_prime(self, length=3):
        """
            equal q in the diagram
            should be prime
        """
        return utils.generate_number(length)

    def get_public_key(self):
        """
            i will send it to the another party.
        """
        return pow(self.generte_generator, self.generte_private_key) % self.generte_prime

    def get_secret_key(self, public_key):
        """
            public_key from the another party.
        """
        return pow(public_key, self.generte_private_key) % self.generte_prime
