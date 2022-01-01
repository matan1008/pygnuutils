from io import BytesIO

import pytest

from pygnuutils.basenc import Basenc, BasencStub, BasencDecodeError


class BasencTestStub(BasencStub):
    def __init__(self):
        self.input_file = BytesIO()
        self.stdout = BytesIO()

    def open(self, file, mode):
        return self.input_file

    @property
    def stdout_buffer(self):
        return self.stdout


@pytest.mark.parametrize('input_, output', [
    (b'test', b'dGVzdA==\n'),
    (
            b'test,test,pytest,te\x00t,test,test,python,test,test,test,test,egg,test,~est,test,test,test,test,abcd',
            (
                    b'dGVzdCx0ZXN0LHB5dGVzdCx0ZQB0LHRlc3QsdGVzdCxweXRob24sdGVzdCx0ZXN0LHRlc3QsdGVz\n'
                    b'dCxlZ2csdGVzdCx+ZXN0LHRlc3QsdGVzdCx0ZXN0LHRlc3QsYWJjZA==\n'
            )
    ),
])
def test_encode_base64(input_, output):
    stub = BasencTestStub()
    stub.input_file = BytesIO(input_)
    basenc = Basenc(stub)
    basenc('placeholder', base64=True)
    assert stub.stdout.getvalue() == output


@pytest.mark.parametrize('input_, output', [
    (b'test', b'dGVzdA==\n'),
    (
            b'test,test,pytest,te\x00t,test,test,python,test,test,test,test,egg,test,~est,test,test,test,test,abcd',
            (
                    b'dGVzdCx0ZXN0LHB5dGVzdCx0ZQB0LHRlc3QsdGVzdCxweXRob24sdGVzdCx0ZXN0LHRlc3QsdGVz\n'
                    b'dCxlZ2csdGVzdCx-ZXN0LHRlc3QsdGVzdCx0ZXN0LHRlc3QsYWJjZA==\n'
            )
    ),
])
def test_encode_base64_url(input_, output):
    stub = BasencTestStub()
    stub.input_file = BytesIO(input_)
    basenc = Basenc(stub)
    basenc('placeholder', base64url=True)
    assert stub.stdout.getvalue() == output


@pytest.mark.parametrize('input_, output', [
    (b'test', b'ORSXG5A=\n'),
    (
            b'test,test,pytest,te\x00t,test,test,python,test,test,test,test,egg,test,~est,test,test,test,test,abcd',
            (
                    b'ORSXG5BMORSXG5BMOB4XIZLTOQWHIZIAOQWHIZLTOQWHIZLTOQWHA6LUNBXW4LDUMVZXILDUMVZX\n'
                    b'ILDUMVZXILDUMVZXILDFM5TSY5DFON2CY7TFON2CY5DFON2CY5DFON2CY5DFON2CY5DFON2CYYLC\n'
                    b'MNSA====\n'
            )
    ),
])
def test_encode_base32(input_, output):
    stub = BasencTestStub()
    stub.input_file = BytesIO(input_)
    basenc = Basenc(stub)
    basenc('placeholder', base32=True)
    assert stub.stdout.getvalue() == output


@pytest.mark.parametrize('input_, output', [
    (b'test', b'EHIN6T0=\n'),
    (
            b'test,test,pytest,te\x00t,test,test,python,test,test,test,test,egg,test,~est,test,test,test,test,abcd',
            (
                    b'EHIN6T1CEHIN6T1CE1SN8PBJEGM78P80EGM78PBJEGM78PBJEGM70UBKD1NMSB3KCLPN8B3KCLPN\n'
                    b'8B3KCLPN8B3KCLPN8B35CTJIOT35EDQ2OVJ5EDQ2OT35EDQ2OT35EDQ2OT35EDQ2OT35EDQ2OOB2\n'
                    b'CDI0====\n'
            )
    ),
])
def test_encode_base32_hex(input_, output):
    stub = BasencTestStub()
    stub.input_file = BytesIO(input_)
    basenc = Basenc(stub)
    basenc('placeholder', base32hex=True)
    assert stub.stdout.getvalue() == output


@pytest.mark.parametrize('input_, output', [
    (b'test', b'74657374\n'),
    (
            b'test,test,pytest,te\x00t,test,test,python,test,test,test,test,egg,test,~est,test,test,test,test,abcd',
            (
                    b'746573742C746573742C7079746573742C746500742C746573742C746573742C707974686F6E\n'
                    b'2C746573742C746573742C746573742C746573742C6567672C746573742C7E6573742C746573\n'
                    b'742C746573742C746573742C746573742C61626364\n'
            )
    ),
])
def test_encode_base16(input_, output):
    stub = BasencTestStub()
    stub.input_file = BytesIO(input_)
    basenc = Basenc(stub)
    basenc('placeholder', base16=True)
    assert stub.stdout.getvalue() == output


@pytest.mark.parametrize('input_, output', [
    (b'test', b'01110100011001010111001101110100\n'),
    (
            b'test,test,pytest,te\x00t,test,test,python,test,test,test,test,egg,test,~est,test,test,test,test,abcd',
            (
                    b'0111010001100101011100110111010000101100011101000110010101110011011101000010\n'
                    b'1100011100000111100101110100011001010111001101110100001011000111010001100101\n'
                    b'0000000001110100001011000111010001100101011100110111010000101100011101000110\n'
                    b'0101011100110111010000101100011100000111100101110100011010000110111101101110\n'
                    b'0010110001110100011001010111001101110100001011000111010001100101011100110111\n'
                    b'0100001011000111010001100101011100110111010000101100011101000110010101110011\n'
                    b'0111010000101100011001010110011101100111001011000111010001100101011100110111\n'
                    b'0100001011000111111001100101011100110111010000101100011101000110010101110011\n'
                    b'0111010000101100011101000110010101110011011101000010110001110100011001010111\n'
                    b'0011011101000010110001110100011001010111001101110100001011000110000101100010\n'
                    b'0110001101100100\n'
            )
    ),
])
def test_encode_base2_msbf(input_, output):
    stub = BasencTestStub()
    stub.input_file = BytesIO(input_)
    basenc = Basenc(stub)
    basenc('placeholder', base2msbf=True)
    assert stub.stdout.getvalue() == output


@pytest.mark.parametrize('input_, output', [
    (b'test', b'00101110101001101100111000101110\n'),
    (
            b'test,test,pytest,te\x00t,test,test,python,test,test,test,test,egg,test,~est,test,test,test,test,abcd',
            (
                    b'0010111010100110110011100010111000110100001011101010011011001110001011100011\n'
                    b'0100000011101001111000101110101001101100111000101110001101000010111010100110\n'
                    b'0000000000101110001101000010111010100110110011100010111000110100001011101010\n'
                    b'0110110011100010111000110100000011101001111000101110000101101111011001110110\n'
                    b'0011010000101110101001101100111000101110001101000010111010100110110011100010\n'
                    b'1110001101000010111010100110110011100010111000110100001011101010011011001110\n'
                    b'0010111000110100101001101110011011100110001101000010111010100110110011100010\n'
                    b'1110001101000111111010100110110011100010111000110100001011101010011011001110\n'
                    b'0010111000110100001011101010011011001110001011100011010000101110101001101100\n'
                    b'1110001011100011010000101110101001101100111000101110001101001000011001000110\n'
                    b'1100011000100110\n'
            )
    ),
])
def test_encode_base2_lsbf(input_, output):
    stub = BasencTestStub()
    stub.input_file = BytesIO(input_)
    basenc = Basenc(stub)
    basenc('placeholder', base2lsbf=True)
    assert stub.stdout.getvalue() == output


@pytest.mark.parametrize('input_, output', [
    (b'test', b'By/Jn\n'),
    (
            b'test,test,pytest,te\x00t,test,test,python,test,test,test,test,egg,test,~est,test,test,test,test,abcd',
            (
                    b'By/JneoCDABs.xRBy/JneoCC6Bs.JBB95%PwPI@AAcVLsz/daFwPI@ABy/JneoCDABs.JBB95%Ax\n'
                    b'j&=qwPI@AER0OxeoCDABs.JBB95%PwPI@ABy/JnemA0$wb\n'
            )
    ),
])
def test_encode_z85(input_, output):
    stub = BasencTestStub()
    stub.input_file = BytesIO(input_)
    basenc = Basenc(stub)
    basenc('placeholder', z85=True)
    assert stub.stdout.getvalue() == output


@pytest.mark.parametrize('input_, output', [
    (b'dGVzdA==', b'test'),
    (
            b'dGVzdCx0ZXN0LHB5dGVzdCx0ZQB0LHRlc3QsdGVzdCxweXRob24sdGVzdCx0ZXN0LHRlc3QsdGVzdCxlZ2csdGVzdCx+ZXN0LHRlc3Q'
            b'sdGVzdCx0ZXN0LHRlc3QsYWJjZA==',
            b'test,test,pytest,te\x00t,test,test,python,test,test,test,test,egg,test,~est,test,test,test,test,abcd'
    ),
])
def test_decode_base64(input_, output):
    stub = BasencTestStub()
    stub.input_file = BytesIO(input_)
    basenc = Basenc(stub)
    basenc('placeholder', base64=True, decode=True)
    assert stub.stdout.getvalue() == output


@pytest.mark.parametrize('input_, output', [
    (b'dGVzdA==', b'test'),
    (
            (
                    b'dGVzdCx0ZXN0LHB5dGVzdCx0ZQB0LHRlc3QsdGVzdCxweXRob24sdGVzdCx0ZXN0LHRlc3QsdGVz'
                    b'dCxlZ2csdGVzdCx-ZXN0LHRlc3QsdGVzdCx0ZXN0LHRlc3QsYWJjZA=='
            ),
            b'test,test,pytest,te\x00t,test,test,python,test,test,test,test,egg,test,~est,test,test,test,test,abcd'
    ),
])
def test_decode_base64_url(input_, output):
    stub = BasencTestStub()
    stub.input_file = BytesIO(input_)
    basenc = Basenc(stub)
    basenc('placeholder', base64url=True, decode=True)
    assert stub.stdout.getvalue() == output


@pytest.mark.parametrize('input_, output', [
    (b'ORSXG5A=', b'test'),
    (
            (
                    b'ORSXG5BMORSXG5BMOB4XIZLTOQWHIZIAOQWHIZLTOQWHIZLTOQWHA6LUNBXW4LDUMVZXILDUMVZX'
                    b'ILDUMVZXILDUMVZXILDFM5TSY5DFON2CY7TFON2CY5DFON2CY5DFON2CY5DFON2CY5DFON2CYYLC'
                    b'MNSA===='
            ),
            b'test,test,pytest,te\x00t,test,test,python,test,test,test,test,egg,test,~est,test,test,test,test,abcd'
    ),
])
def test_decode_base32(input_, output):
    stub = BasencTestStub()
    stub.input_file = BytesIO(input_)
    basenc = Basenc(stub)
    basenc('placeholder', base32=True, decode=True)
    assert stub.stdout.getvalue() == output


@pytest.mark.parametrize('input_, output', [
    (b'EHIN6T0=', b'test'),
    (
            (
                    b'EHIN6T1CEHIN6T1CE1SN8PBJEGM78P80EGM78PBJEGM78PBJEGM70UBKD1NMSB3KCLPN8B3KCLPN'
                    b'8B3KCLPN8B3KCLPN8B35CTJIOT35EDQ2OVJ5EDQ2OT35EDQ2OT35EDQ2OT35EDQ2OT35EDQ2OOB2'
                    b'CDI0===='
            ),
            b'test,test,pytest,te\x00t,test,test,python,test,test,test,test,egg,test,~est,test,test,test,test,abcd'
    ),
])
def test_decode_base32_hex(input_, output):
    stub = BasencTestStub()
    stub.input_file = BytesIO(input_)
    basenc = Basenc(stub)
    basenc('placeholder', base32hex=True, decode=True)
    assert stub.stdout.getvalue() == output


@pytest.mark.parametrize('input_, output', [
    (b'74657374', b'test'),
    (
            (
                    b'746573742C746573742C7079746573742C746500742C746573742C746573742C707974686F6E'
                    b'2C746573742C746573742C746573742C746573742C6567672C746573742C7E6573742C746573'
                    b'742C746573742C746573742C746573742C61626364'
            ),
            b'test,test,pytest,te\x00t,test,test,python,test,test,test,test,egg,test,~est,test,test,test,test,abcd'
    ),
])
def test_decode_base16(input_, output):
    stub = BasencTestStub()
    stub.input_file = BytesIO(input_)
    basenc = Basenc(stub)
    basenc('placeholder', base16=True, decode=True)
    assert stub.stdout.getvalue() == output


@pytest.mark.parametrize('input_, output', [
    (b'01110100011001010111001101110100', b'test'),
    (
            (
                    b'0111010001100101011100110111010000101100011101000110010101110011011101000010'
                    b'1100011100000111100101110100011001010111001101110100001011000111010001100101'
                    b'0000000001110100001011000111010001100101011100110111010000101100011101000110'
                    b'0101011100110111010000101100011100000111100101110100011010000110111101101110'
                    b'0010110001110100011001010111001101110100001011000111010001100101011100110111'
                    b'0100001011000111010001100101011100110111010000101100011101000110010101110011'
                    b'0111010000101100011001010110011101100111001011000111010001100101011100110111'
                    b'0100001011000111111001100101011100110111010000101100011101000110010101110011'
                    b'0111010000101100011101000110010101110011011101000010110001110100011001010111'
                    b'0011011101000010110001110100011001010111001101110100001011000110000101100010'
                    b'0110001101100100'
            ),
            b'test,test,pytest,te\x00t,test,test,python,test,test,test,test,egg,test,~est,test,test,test,test,abcd'
    ),
])
def test_decode_base2_msbf(input_, output):
    stub = BasencTestStub()
    stub.input_file = BytesIO(input_)
    basenc = Basenc(stub)
    basenc('placeholder', base2msbf=True, decode=True)
    assert stub.stdout.getvalue() == output


@pytest.mark.parametrize('input_, output', [
    (b'00101110101001101100111000101110', b'test'),
    (
            (
                    b'0010111010100110110011100010111000110100001011101010011011001110001011100011'
                    b'0100000011101001111000101110101001101100111000101110001101000010111010100110'
                    b'0000000000101110001101000010111010100110110011100010111000110100001011101010'
                    b'0110110011100010111000110100000011101001111000101110000101101111011001110110'
                    b'0011010000101110101001101100111000101110001101000010111010100110110011100010'
                    b'1110001101000010111010100110110011100010111000110100001011101010011011001110'
                    b'0010111000110100101001101110011011100110001101000010111010100110110011100010'
                    b'1110001101000111111010100110110011100010111000110100001011101010011011001110'
                    b'0010111000110100001011101010011011001110001011100011010000101110101001101100'
                    b'1110001011100011010000101110101001101100111000101110001101001000011001000110'
                    b'1100011000100110'
            ),
            b'test,test,pytest,te\x00t,test,test,python,test,test,test,test,egg,test,~est,test,test,test,test,abcd'
    ),
])
def test_decode_base2_lsbf(input_, output):
    stub = BasencTestStub()
    stub.input_file = BytesIO(input_)
    basenc = Basenc(stub)
    basenc('placeholder', base2lsbf=True, decode=True)
    assert stub.stdout.getvalue() == output


@pytest.mark.parametrize('input_, output', [
    (b'By/Jn', b'test'),
    (
            (
                    b'By/JneoCDABs.xRBy/JneoCC6Bs.JBB95%PwPI@AAcVLsz/daFwPI@ABy/JneoCDABs.JBB95%Ax'
                    b'j&=qwPI@AER0OxeoCDABs.JBB95%PwPI@ABy/JnemA0$wb'
            ),
            b'test,test,pytest,te\x00t,test,test,python,test,test,test,test,egg,test,~est,test,test,test,test,abcd'
    ),
])
def test_decode_z85(input_, output):
    stub = BasencTestStub()
    stub.input_file = BytesIO(input_)
    basenc = Basenc(stub)
    basenc('placeholder', z85=True, decode=True)
    assert stub.stdout.getvalue() == output


@pytest.mark.parametrize('input_, output', [
    (b'dGVzdA==\n', b'test'),
    (
            b'dGVzdCx0ZXN0LHB5dGVzdCx0ZQB0LHRlc3QsdGVzdCxweXRob24sdGVzdCx0ZXN0LHRlc3QsdGVzdCxlZ2csdGVzdCx+ZXN0LHRlc3Q\n'
            b'sdGVzdCx0ZXN0LHRlc3QsYWJjZA==\n',
            b'test,test,pytest,te\x00t,test,test,python,test,test,test,test,egg,test,~est,test,test,test,test,abcd'
    ),
])
def test_decode_base64_ignore_garbage(input_, output):
    stub = BasencTestStub()
    stub.input_file = BytesIO(input_)
    basenc = Basenc(stub)
    with pytest.raises(BasencDecodeError):
        basenc('placeholder', base64=True, decode=True)
    stub.input_file = BytesIO(input_)
    basenc('placeholder', base64=True, decode=True, ignore_garbage=True)
    assert stub.stdout.getvalue() == output


@pytest.mark.parametrize('input_, output', [
    (b'dGVzdA==\n', b'test'),
    (
            (
                    b'dGVzdCx0ZXN0LHB5dGVzdCx0ZQB0LHRlc3QsdGVzdCxweXRob24sdGVzdCx0ZXN0LHRlc3QsdGVz\n'
                    b'dCxlZ2csdGVzdCx-ZXN0LHRlc3QsdGVzdCx0ZXN0LHRlc3QsYWJjZA==\n'
            ),
            b'test,test,pytest,te\x00t,test,test,python,test,test,test,test,egg,test,~est,test,test,test,test,abcd'
    ),
])
def test_decode_base64_url_ignore_garbage(input_, output):
    stub = BasencTestStub()
    stub.input_file = BytesIO(input_)
    basenc = Basenc(stub)
    with pytest.raises(BasencDecodeError):
        basenc('placeholder', base64url=True, decode=True)
    stub.input_file = BytesIO(input_)
    basenc('placeholder', base64url=True, decode=True, ignore_garbage=True)
    assert stub.stdout.getvalue() == output


@pytest.mark.parametrize('input_, output', [
    (b'ORSXG5A=\n', b'test'),
    (
            (
                    b'ORSXG5BMORSXG5BMOB4XIZLTOQWHIZIAOQWHIZLTOQWHIZLTOQWHA6LUNBXW4LDUMVZXILDUMVZX\n'
                    b'ILDUMVZXILDUMVZXILDFM5TSY5DFON2CY7TFON2CY5DFON2CY5DFON2CY5DFON2CY5DFON2CYYLC\n'
                    b'MNSA====\n'
            ),
            b'test,test,pytest,te\x00t,test,test,python,test,test,test,test,egg,test,~est,test,test,test,test,abcd'
    ),
])
def test_decode_base32_ignore_garbage(input_, output):
    stub = BasencTestStub()
    stub.input_file = BytesIO(input_)
    basenc = Basenc(stub)
    with pytest.raises(BasencDecodeError):
        basenc('placeholder', base32=True, decode=True)
    stub.input_file = BytesIO(input_)
    basenc('placeholder', base32=True, decode=True, ignore_garbage=True)
    assert stub.stdout.getvalue() == output


@pytest.mark.parametrize('input_, output', [
    (b'EHIN6T0=\n', b'test'),
    (
            (
                    b'EHIN6T1CEHIN6T1CE1SN8PBJEGM78P80EGM78PBJEGM78PBJEGM70UBKD1NMSB3KCLPN8B3KCLPN\n'
                    b'8B3KCLPN8B3KCLPN8B35CTJIOT35EDQ2OVJ5EDQ2OT35EDQ2OT35EDQ2OT35EDQ2OT35EDQ2OOB2\n'
                    b'CDI0====\n'
            ),
            b'test,test,pytest,te\x00t,test,test,python,test,test,test,test,egg,test,~est,test,test,test,test,abcd'
    ),
])
def test_decode_base32_hex_ignore_garbage(input_, output):
    stub = BasencTestStub()
    stub.input_file = BytesIO(input_)
    basenc = Basenc(stub)
    with pytest.raises(BasencDecodeError):
        basenc('placeholder', base32hex=True, decode=True)
    stub.input_file = BytesIO(input_)
    basenc('placeholder', base32hex=True, decode=True, ignore_garbage=True)
    assert stub.stdout.getvalue() == output


@pytest.mark.parametrize('input_, output', [
    (b'74657374\n', b'test'),
    (
            (
                    b'746573742C746573742C7079746573742C746500742C746573742C746573742C707974686F6E\n'
                    b'2C746573742C746573742C746573742C746573742C6567672C746573742C7E6573742C746573\n'
                    b'742C746573742C746573742C746573742C61626364\n'
            ),
            b'test,test,pytest,te\x00t,test,test,python,test,test,test,test,egg,test,~est,test,test,test,test,abcd'
    ),
])
def test_decode_base16_ignore_garbage(input_, output):
    stub = BasencTestStub()
    stub.input_file = BytesIO(input_)
    basenc = Basenc(stub)
    with pytest.raises(BasencDecodeError):
        basenc('placeholder', base16=True, decode=True)
    stub.input_file = BytesIO(input_)
    basenc('placeholder', base16=True, decode=True, ignore_garbage=True)
    assert stub.stdout.getvalue() == output


@pytest.mark.parametrize('input_, output', [
    (b'01110100011001010111001101110100\n', b'test'),
    (
            (
                    b'0111010001100101011100110111010000101100011101000110010101110011011101000010\n'
                    b'1100011100000111100101110100011001010111001101110100001011000111010001100101\n'
                    b'0000000001110100001011000111010001100101011100110111010000101100011101000110\n'
                    b'0101011100110111010000101100011100000111100101110100011010000110111101101110\n'
                    b'0010110001110100011001010111001101110100001011000111010001100101011100110111\n'
                    b'0100001011000111010001100101011100110111010000101100011101000110010101110011\n'
                    b'0111010000101100011001010110011101100111001011000111010001100101011100110111\n'
                    b'0100001011000111111001100101011100110111010000101100011101000110010101110011\n'
                    b'0111010000101100011101000110010101110011011101000010110001110100011001010111\n'
                    b'0011011101000010110001110100011001010111001101110100001011000110000101100010\n'
                    b'0110001101100100\n'
            ),
            b'test,test,pytest,te\x00t,test,test,python,test,test,test,test,egg,test,~est,test,test,test,test,abcd'
    ),
])
def test_decode_base2_msbf_ignore_garbage(input_, output):
    stub = BasencTestStub()
    stub.input_file = BytesIO(input_)
    basenc = Basenc(stub)
    with pytest.raises(BasencDecodeError):
        basenc('placeholder', base2msbf=True, decode=True)
    stub.input_file = BytesIO(input_)
    basenc('placeholder', base2msbf=True, decode=True, ignore_garbage=True)
    assert stub.stdout.getvalue() == output


@pytest.mark.parametrize('input_, output', [
    (b'00101110101001101100111000101110\n', b'test'),
    (
            (
                    b'0010111010100110110011100010111000110100001011101010011011001110001011100011\n'
                    b'0100000011101001111000101110101001101100111000101110001101000010111010100110\n'
                    b'0000000000101110001101000010111010100110110011100010111000110100001011101010\n'
                    b'0110110011100010111000110100000011101001111000101110000101101111011001110110\n'
                    b'0011010000101110101001101100111000101110001101000010111010100110110011100010\n'
                    b'1110001101000010111010100110110011100010111000110100001011101010011011001110\n'
                    b'0010111000110100101001101110011011100110001101000010111010100110110011100010\n'
                    b'1110001101000111111010100110110011100010111000110100001011101010011011001110\n'
                    b'0010111000110100001011101010011011001110001011100011010000101110101001101100\n'
                    b'1110001011100011010000101110101001101100111000101110001101001000011001000110\n'
                    b'1100011000100110\n'
            ),
            b'test,test,pytest,te\x00t,test,test,python,test,test,test,test,egg,test,~est,test,test,test,test,abcd'
    ),
])
def test_decode_base2_lsbf_ignore_garbage(input_, output):
    stub = BasencTestStub()
    stub.input_file = BytesIO(input_)
    basenc = Basenc(stub)
    with pytest.raises(BasencDecodeError):
        basenc('placeholder', base2lsbf=True, decode=True)
    stub.input_file = BytesIO(input_)
    basenc('placeholder', base2lsbf=True, decode=True, ignore_garbage=True)
    assert stub.stdout.getvalue() == output


@pytest.mark.parametrize('input_, output', [
    (b'By/Jn\n', b'test'),
    (
            (
                    b'By/JneoCDABs.xRBy/JneoCC6Bs.JBB95%PwPI@AAcVLsz/daFwPI@ABy/JneoCDABs.JBB95%Ax\n'
                    b'j&=qwPI@AER0OxeoCDABs.JBB95%PwPI@ABy/JnemA0$wb\n'
            ),
            b'test,test,pytest,te\x00t,test,test,python,test,test,test,test,egg,test,~est,test,test,test,test,abcd'
    ),
])
def test_decode_z85_ignore_garbage(input_, output):
    stub = BasencTestStub()
    stub.input_file = BytesIO(input_)
    basenc = Basenc(stub)
    with pytest.raises(BasencDecodeError):
        basenc('placeholder', z85=True, decode=True)
    stub.input_file = BytesIO(input_)
    basenc('placeholder', z85=True, decode=True, ignore_garbage=True)
    assert stub.stdout.getvalue() == output


@pytest.mark.parametrize('input_, output, wrap', [
    (
            b'test,test,pytest,te\x00t,test,test,python,test,test,test,test,egg,test,~est,test,test,test,test,abcd',
            (
                    b'dGVzdCx0ZXN0LHB5dGVzdCx0ZQB0LHRlc3QsdGVzdCxweXRob24sdGVzdCx0ZXN0LHRlc3QsdGVz'
                    b'dCxlZ2csdGVzdCx+ZXN0LHRlc3QsdGVzdCx0ZXN0LHRlc3QsYWJjZA=='
            ),
            0
    ),
    (
            b'test,test,pytest,te\x00t,test,test,python,test,test,test,test,egg,test,~est,test,test,test,test,abcd',
            (
                    b'dGVzdCx0ZXN0LHB5dGVz\n'
                    b'dCx0ZQB0LHRlc3QsdGVz\n'
                    b'dCxweXRob24sdGVzdCx0\n'
                    b'ZXN0LHRlc3QsdGVzdCxl\n'
                    b'Z2csdGVzdCx+ZXN0LHRl\n'
                    b'c3QsdGVzdCx0ZXN0LHRl\n'
                    b'c3QsYWJjZA==\n'
            ),
            20
    ),
])
def test_encode_wrap(input_, output, wrap):
    stub = BasencTestStub()
    stub.input_file = BytesIO(input_)
    basenc = Basenc(stub)
    basenc('placeholder', base64=True, wrap=wrap)
    assert stub.stdout.getvalue() == output
