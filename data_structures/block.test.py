# imports
import unittest
from block import * 
import time

# unit test class
class TestBlock(unittest.TestCase):

    # test hash function

    def testHashSHA(self):
        # testHashSHA part 1:
        # take two different strings
        # check to see if hashes are different
        a = "apple"
        b = "orange"
        hashA = hashSHA(a)        
        hashB = hashSHA(b)
        self.assertNotEqual(hashA, hashB)

        # testHashSHA part 2:
        # take two long strings with a single letter changed
        # check to see if hashes are different
        s1 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        s2 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minin veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        hashS1 = hashSHA(s1)
        hashS2 = hashSHA(s2)
        self.assertNotEqual(hashS1, hashS2)

        # testHashSHA part 3:
        # take two of the same strings
        # hash them separately
        # check to see if the hashes are equivalent
        c = "melon"
        d = "melon"
        hashC = hashSHA(c)
        hashD = hashSHA(d)
        self.assertEqual(hashC, hashD)

    # test is valid
    # check to see if a block points backwards to a previous block
    def testIsValid(self):
        blockA = createBlock('this is block a', '000')
        blockB = createBlock('this is block b', blockA['blockHash'])
        self.assertTrue(isValid(blockA, blockB))

    # test add block
    # check to see if when adding a block it is contained in the chain
    def testAddBlock(self):
        bc = Blockchain()
        testBlock = createBlock('this is a test', '123456789')
        bc.addBlock(testBlock)
        self.assertEqual(bc.chain[0], testBlock)


    # test top
    # check to see if calling top returns the last block in the chain
    def testTop(self):
        bc = Blockchain()
        testBlock = createBlock('this is a test', '123456789')
        bc.addBlock(testBlock)
        self.assertEqual(bc.top(), testBlock)

    # test height
    # check to see if height returns the length of the chain
    def testHeight(self):
        bc = Blockchain()
        testBlock = createBlock('this is a test', '123456789')
        bc.addBlock(testBlock)
        bc.addBlock(testBlock)
        bc.addBlock(testBlock)
        bc.addBlock(testBlock)
        self.assertEqual(4, bc.height())

    # test proof of work
    # check to see if a proof of work mined block
    # contains a hash that's less than the target
    def testPoW(self):
        data = 'testPoW'
        prevHash = '000000'
        target = 10**70       # play around with this exponent (stick to the 60-100 range)
        print("Mining...")
        a = int(time.time())
        b = createBlockPoW(data, prevHash, target)
        print("Block found!")
        c = int(time.time())
        print("Time it took: {} seconds".format((c-a)))
        self.assertLessEqual(toInt(b['blockHash']), target)



if __name__ == '__main__':
    unittest.main()
