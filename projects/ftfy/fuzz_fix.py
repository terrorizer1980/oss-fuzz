#!/usr/bin/python3
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import atheris
import sys
with atheris.instrument_imports():
    import ftfy

def TestInput(data):
    fdp = atheris.FuzzedDataProvider(data)

    try:
        ftfy.fix_text(fdp.ConsumeString(1000))
        ftfy.fix_text(fdp.ConsumeUnicode(1000))

        plan1 = ftfy.fix_and_explain(fdp.ConsumeString(1000))[1]
        plan2 = ftfy.fix_and_explain(fdp.ConsumeUnicode(1000))[1]
        ftfy.apply_plan(fdp.ConsumeString(1000), plan1)
        ftfy.apply_plan(fdp.ConsumeString(1000), plan2)
        ftfy.apply_plan(fdp.ConsumeUnicode(1000), plan1)
        ftfy.apply_plan(fdp.ConsumeUnicode(1000), plan2)

        ftfy.fix_text_segment(fdp.ConsumeString(1000))
        ftfy.fix_text_segment(fdp.ConsumeUnicode(1000))

        f = open("temp.txt", "w")
        f.write(fdp.ConsumeString(1000))
        f.write(fdp.ConsumeUnicode(1000))
        f.close()
        f = open("temp.txt", "r")
        ftfy.fix_file(f)
        f.close()

        ftfy.guess_bytes(fdp.ConsumeBytes(1000))
    except UnicodeError as e:
        if "Hey wait, this isn't Unicode." not in str(e):
            raise e

def main():
    atheris.Setup(sys.argv, TestInput, enable_python_coverage=True)
    atheris.Fuzz()

if __name__ == "__main__":
    main()
