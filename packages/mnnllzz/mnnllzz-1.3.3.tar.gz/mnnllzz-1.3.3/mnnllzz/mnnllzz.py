#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import shutil
import glob
import re
import string
import json
from subprocess import PIPE, run

import random
from decimal import Decimal
import numpy as np
from numpy import sqrt, exp, sin, cos, tan, log, log10, pi, floor, abs

# https://stackoverflow.com/questions/15933741/how-do-i-catch-a-numpy-warning-like-its-an-exception-not-just-for-testing
np.seterr(all="raise")

#%% Class definition.

class RandomSearchStuck(Exception):
    def __init__(self, msg):
        self.msg = msg


class ExamTest():

    def __init__(self,
                 template_text, testnr,
                 solutions,
                 year, month, day,
                 salt_1, salt_2,
                 mark_sol=False):
        # A string containing the whole TeX template.
        self.source_text = template_text
        # The number of this test.
        self.testnr = testnr
        # List of dictionaries with selected values.
        self.values = []
        # List of lists of dictionaries with the solutions.
        self.solutions = solutions
        # The date.
        self.test_year = year
        self.test_month = month
        self.test_day = day
        # Whether to mark correct solutions.
        self.mark_sol = mark_sol
        # Set seeds for the random numbers based on the test number.
        random.seed(salt_1 * (testnr + 1))  # for the letters
        np.random.seed(salt_2 * (testnr + 1))   # for the values
        # Constant: uppercase alphabet.
        self._letters = string.ascii_uppercase


    def results_init(self):
        # The literal substitutions to be made in the TeX template.
        self.subst = {}
        self.subst["TESTNR"] = "%d" % self.testnr
        self.subst["ANNO"] = "%04d" % self.test_year
        self.subst["MESE"] = "%02d" % self.test_month
        self.subst["GIORNO"] = "%02d" % self.test_day
        # The variables in the problems.
        self.x = {}
        # The constants in the problems.
        self.c = {}
        # Truth values for the constraints.
        self.constraints = []
        # The letters of the solution.
        self.sol_letters = []
        # The values of the solution.
        self.sol_values = []


    def apply_subst(self):
        # Check that no key in the substitution dictionary matches another one.
        # For example, the key "MASS" matches "MASS1", which would produce an
        # erroneous expression in the text after substitution.
        keys_OK = True
        keys_list = list(self.subst.keys())
        for key in keys_list:
            for key1 in keys_list:
                if (key != key1):  # it is the same key if the strings are equal
                    if (key in key1):
                        print("CONFUSING LABELS: %s matches %s." % (key, key1))
                        keys_OK = False
                        break  # break from inner loop
            if (not keys_OK):
                break  # break from outer loop

        if keys_OK:
            # Create a regular expression  from the dictionary keys
            all_labels = re.compile("(%s)" % "|".join(map(re.escape, self.subst.keys())))
            # For each match, look-up corresponding value in dictionary
            self.source_text = all_labels.sub(
                lambda mo: self.subst[mo.string[mo.start():mo.end()]], self.source_text)


    def fexp(self, number):
        # Calculate the exponent of a number, base 10.
        (sign, digits, exponent) = Decimal(number).as_tuple()
        r = len(digits) + exponent - 1
        return r


    def fman(self, number):
        # Calculate the mantissa of a number, base 10.
        r = Decimal(number).scaleb(-self.fexp(number)).normalize()
        return r


    def number_format(self, val):
        # Format a number in different ways based on its length.
        # Always use 3 significant digits.
        m = self.fman(val)  # mantissa
        e = self.fexp(val)  # exponent
        if (e == 0):  # 1.23
            r = r"\ensuremath{%.2f}" % val
        elif (e == 1):  # 12.3
            r = r"\ensuremath{%.1f}" % val
        elif (e == 2):  # 123
            r = r"\ensuremath{%.0f}" % val
        elif (e == -1):  # 0.123
            r = r"\ensuremath{%.3f}" % val
        elif (e == -2):  # 0.0123
            r = r"\ensuremath{%.4f}" % val
        else:
            r = r"\ensuremath{%.2f \times 10^{%d}}" % (m, e)
        return r


    def eval_check(self, str_expr, label):
        x = self.x
        c = self.c
        try:
            r = eval(str_expr)
        except (RuntimeWarning, OverflowError, ValueError, FloatingPointError):
            print("\n\nEvaluation error in %s" % label)
            print(json.dumps(self.values, sort_keys=True, indent=4))
            sys.exit("Stop.")
        return r


    def const_set(self, name, label, val):
        # Save the value to the dictionary of values.
        self.c[name] = val
        # Save the replacement to be made in the template.
        self.subst[label] = self.number_format(val)


    def trn(self, val, dig=3):
        # Truncate number to num significat digits.
        m = float(self.fman(val))  # mantissa
        e = float(self.fexp(val))  # exponent
        m = int(m * 10.0**(dig-1.0)) / 10.0**(dig-1.0)
        r = m * 10.0**e
        return r


    def save_to_values(self, name=None, val=None, new=False):
        if (new):
            self.values.append({})
        else:
            self.values[-1][name] = val


    def param_set(self, name, label, valmin, valmax):
        # Calculate a random value for the parameter.
        val = self.trn(np.random.uniform(valmin, valmax), dig=2)
        # Save the value to the dictionary of values.
        self.x[name] = val
        self.save_to_values(name, val)
        # Save the replacement to be made in the template.
        self.subst[label] = self.number_format(val)


    def random_options(self, valsol, num=5, val_range=None, exp_range_width=None):
        # Choose num values uniformly distributed between valmin and valmax.
        # Reject values which are too close to each other or the solution.
        # List containing the values, including the solution.
        vv = []
        vv.append(valsol)
        # Decide which random distribution to use.
        if (val_range is not None):
            distro = "uniform"
        elif (exp_range_width is not None):
            distro = "log"

        # Calculate range of random options.
        if (distro == "uniform"):
            valmin = val_range[0]
            valmax = val_range[1]
        elif (distro == "log"):
            exp_max = np.random.uniform(0.0, exp_range_width)
            exp_min = exp_max - exp_range_width
            val_1 = valsol * (10.0 ** exp_min)
            val_2 = valsol * (10.0 ** exp_max)
            valmin = np.minimum(val_1, val_2)
            valmax = np.maximum(val_1, val_2)

        # The minimum acceptable difference between two values.
        delta1 = np.abs(valsol) * 0.05
        delta2 = np.abs(valmax - valmin) * 0.10
        delta = np.maximum(delta1, delta2)

        i_try = 0
        v_try_hist = []
        while (len(vv) < (num+1)):
            # Randomly choose a new value.
            ##if (distro == "uniform"):
            ##    v_try = np.random.uniform(valmin, valmax)
            ##elif (distro == "log"):
            ##    exp_try = np.random.uniform(exp_min, exp_max)
            ##    v_try = valsol * (10.0 ** exp_try)
            v_try = np.random.uniform(valmin, valmax)
            # The minimum difference with the accepted values so far.
            epsilon = np.array([np.abs(v_try - v) for v in vv]).min()
            v_try_hist.append([v_try,] + [np.abs(v_try - v) for v in vv])
            if (epsilon > delta):
                vv.append(v_try)
            i_try = i_try + 1
            # Prevent loop being stuck.
            if (i_try > 100):
                print(delta1, delta2)
                for t in v_try_hist:
                    print(t)
                data = "Loop stuck in random_options\nSol: %e, Min: %e, Max: %e\n" % (valsol, valmin, valmax)
                raise RandomSearchStuck(data)
        # Return the list as array.  Do not include the first value, which is
        # the solution.
        xx = np.array(vv[1:])
        return xx


    def solution_set(self, label_question, x_sol,
                     x_forced=None, keep_sign=True, x_range=None, num=5):
        # Calculate random options.
        try:
            if (x_range is not None):
                xx = self.random_options(x_sol, num=num, val_range=[x_range[0], x_range[1]])
            elif (keep_sign):
                xx = self.random_options(x_sol, num=num, exp_range_width=0.7)
            else:
                xx = self.random_options(x_sol, num=num, exp_range_width=0.7)
                # Change sign to at least 3 numbers, so that if one of them is
                # swapped for the correct solution, we still have at least 2
                # options with each sign.
                num_opp = random.randint(3,(num+1)//2)
                for i in range(num_opp):
                    xx[i] = -xx[i]
                random.shuffle(xx)
        except (RuntimeWarning, OverflowError):
            print("Error in random options of solution %s" % label_question)
            print("%e" % (x_sol))
            sys.exit("Stop.")

        # The available choices.
        avail = list(range(num))
        # Randomly place the solution and remove the chosen position.
        i_sol = random.choice(avail)
        xx[i_sol] = x_sol
        avail.remove(i_sol)
        # Save the solution to an instance list.
        self.sol_values.append(x_sol)
        self.sol_letters.append(self._letters[i_sol])
        # Randomly place the forced (wrong) option.
        if (x_forced is not None):
            i_forced = random.choice(avail)
            xx[i_forced] = x_forced
            avail.remove(i_forced)
        # Save the replacements to be made in the template.
        for i_opt,(val,a) in enumerate(zip(xx,self._letters[:num])):
            # The number for this replacement.
            repl_val = self.number_format(val)
            # The label for this replacement.
            if ((i_opt == i_sol) and self.mark_sol):
                # Replace the box to mark the solution as correct.
                label_choice = r"%s \fbox{%s%s}" % (a,label_question,a)
                subst_choice = r"\parbox[t]{2cm}{%s \fbox{%s}}\hspace{-2cm}\parbox{2cm}{\bf \Large \hspace{-7pt} \raisebox{1pt}{X}}\hspace{-2cm}\phantom{%s \fbox{%s}}" % (
                    a, repl_val, a, repl_val)
            else:
                # Just replace the number.
                label_choice = label_question + a
                subst_choice = repl_val
            # The replacement.
            self.subst[label_choice] = subst_choice


    def values_def(self):
        # Iterate over several trials to satisfy constraints on the output.
        values_found = False
        n_try = 0

        while(not values_found):

            self.results_init()
            n_try = n_try + 1

            # Read the JSON with the values of the parameters to fill in.
            for sol_block in self.solutions:
                self.save_to_values(new=True)
                for op in sol_block:
                    # Constant with a fixed value.
                    if (op["type"] == "constant"):
                        val = self.eval_check(op["value"], "constant %s" % op["name"])
                        self.const_set(op["name"], op["label"], val)
                    # Parameter, with a randomly chosen value.
                    elif (op["type"] == "parameter"):
                        valmin = self.eval_check(op["min"], "min of parameter %s" % op["name"])
                        valmax = self.eval_check(op["max"], "max of parameter %s" % op["name"])
                        self.param_set(op["name"], op["label"], valmin, valmax)
                    # Generic variable needed to calculate the solution.
                    elif (op["type"] == "variable"):
                        val = self.eval_check(op["value"], "variable %s" % op["name"])
                        self.x[op["name"]] = val
                        self.save_to_values(op["name"], val)
                    # Value of the solution, with optional parameters to
                    # determine the set of multiple choices.
                    elif (op["type"] == "solution"):
                        # Check which optional parameters are set in the JSON
                        # end evaluate their values.
                        opt_keys = ["x_forced", "keep_sign", "x_range"]
                        opt_dict = {}
                        for k in opt_keys:
                            if k in op:
                                val = self.eval_check(op[k], "option %s of solution %s" % (k, op["label"]))
                                opt_dict[k] = val
                        # Set the value of the solution and pass optional
                        # arguments to the function.
                        val = self.eval_check(op["value"], "solution %s" % op["label"])
                        self.solution_set(op["label"], val, **opt_dict)
                    elif (op["type"] == "constraint"):
                        val = self.eval_check(op["condition"], "condition")
                        self.constraints.append(val)

            # If we satisfy all constraint, exit the loop and save the dict of
            # substitutions and the lists of solutions.
            if (all(self.constraints)):
                values_found = True
                # Print if this is not the first try.
                if (n_try > 1):
                    print("%03d \033[0;32mConstraints fulfilled after %d tries.\033[0;0m" % (self.testnr, n_try))
            else:
                # Stop the loop anyway.
                if (n_try > 19):
                    values_found = True
                    print("%03d \033[1;31mConstraints not fulfilled.\033[0;0m" % self.testnr)
                    self.subst = {}
                    self.subst["TESTNR"] = "TESTO NON VALIDO"


#%% Definition of typesetting procedure.

def update_progress(progress):
    # https://stackoverflow.com/questions/3160699/python-progress-bar
    barLength = 20
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "Error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rTypesetting: [{0}] {1:3.0f}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()


def typeset_tests(p, template_text):

    # Read the template.
    # with open(p["template_filename"], "r") as f:
    #     template_text = f.read()

    # Prepare directories for the build.
    if os.path.exists("build") and os.path.isdir("build"):
        shutil.rmtree("build")
    if os.path.exists("distribute") and os.path.isdir("distribute"):
        shutil.rmtree("distribute")
    os.mkdir("build")
    os.mkdir("distribute")
    for filename in glob.glob("*.png"):
        shutil.copy(filename, "build")

    # Lists where the solutions of each test are stored.
    sol_letters = []
    sol_values = []
    all_variables = []

    # Iterate over the tests.
    for i_test in np.arange(p["num_tests"]):

        update_progress(i_test/p["num_tests"])

        # Create a test instance, based on the template.
        test_data = ExamTest(
            template_text, i_test + 1, p["solutions"],
            p["test_year"], p["test_month"], p["test_day"],
            p["random_salt_1"], p["random_salt_2"],
            mark_sol=False)

        try:
            # Calculate random parameters and solutions.
            test_data.values_def()
        except RandomSearchStuck as err:
            update_progress(-1.0)
            print("ERROR: Cannot find random values for test %d." % i_test)
            print(err.msg)
            break

        sol_letters.append(test_data.sol_letters)
        sol_values.append(test_data.sol_values)
        all_variables.append(test_data.values)

        # Substitute the random values into the template.
        test_data.apply_subst()

        # Save the complete source TeX file.
        with open(os.path.join("build","temp.tex"), "w") as f:
            f.write(test_data.source_text)

        # Compile the source TeX and move the PDF to a different folder.
        pdfname = "compito_%03d" % test_data.testnr
        os.chdir("build")
        # os.system(f"pdflatex -quiet -jobname={pdfname} temp.tex")
        # os.system(f"pdflatex --interaction=batchmode -jobname={pdfname} temp.tex")
        r = run(f"pdflatex --interaction=batchmode -jobname={pdfname} temp.tex", stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        os.chdir("..")
        shutil.copy(os.path.join("build", f"{pdfname}.pdf"), "distribute")

        # Save all values.
        with open(os.path.join("distribute","all_values.json"), "w") as f:
            f.write(json.dumps(all_variables, sort_keys=True, indent=4))

    update_progress(1.0)


    # Produce test with correct solutions marked.
    if p["solution_test"]:

        # Create a test instance, based on the template.
        test_data = ExamTest(
            template_text, 0, p["solutions"],
            p["test_year"], p["test_month"], p["test_day"],
            p["random_salt_1"], p["random_salt_2"],
            mark_sol=True)

        try:
            # Calculate random parameters and solutions.
            test_data.values_def()

            # Substitute the random values into the template.
            test_data.apply_subst()

            # Save the complete source TeX file.
            with open("build/temp.tex", "w") as f:
                f.write(test_data.source_text)

            # Compile the source TeX and move the PDF to a different folder.
            pdfname = "compito_soluzioni_%04d-%02d-%02d" % (
                p["test_year"], p["test_month"], p["test_day"])
            os.chdir("build")
            # os.system(f"pdflatex -quiet -jobname={pdfname} temp.tex")
            # os.system(f"pdflatex --interaction=batchmode -jobname={pdfname} temp.tex")
            r = run(f"pdflatex --interaction=batchmode -jobname={pdfname} temp.tex", stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
            os.chdir("..")
            shutil.copy(os.path.join("build", f"{pdfname}.pdf"), ".")

        except RandomSearchStuck as err:
            print("ERROR: Cannot find random values for solution test.")
            print(err.msg)


    # Clean the build folder.
    if os.path.exists("build") and os.path.isdir("build"):
        shutil.rmtree("build")

    # Save the letters and the values of the solution.
    # Each row correspond to a test, each column to a question.
    # Use TSV, which makes it easier to copy-paste to a web-based spreadsheet.

    with open(os.path.join("distribute","solution_letters.tsv"), "w") as f:
            f.write("\n".join(["\t".join(letters) for letters in sol_letters]))

    with open(os.path.join("distribute","solution_numbers.tsv"), "w") as f:
            f.write("\n".join(["\t".join(map(lambda x: "%.4E" % x, values)) for values in sol_values]))

