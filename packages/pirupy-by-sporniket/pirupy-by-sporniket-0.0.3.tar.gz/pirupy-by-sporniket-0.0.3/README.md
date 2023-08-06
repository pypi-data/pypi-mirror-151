# PIRUPY : A PIpeline RUnner for PYthon

[![Latest version](https://img.shields.io/github/v/release/sporniket/pirupy?include_prereleases)](https://github.com/sporniket/pirupy/releases)
[![Workflow status](https://img.shields.io/github/workflow/status/sporniket/pirupy/Python%20package)](https://github.com/sporniket/pirupy/actions/workflows/python-package.yml)
[![Download status](https://img.shields.io/pypi/dm/pirupy-by-sporniket)](https://pypi.org/project/pirupy-by-sporniket/)

A set of annotations to define a set of 'jobs' regrouped into a sequence of 'stages', forming a 'pipeline'. Pipelines
and jobs have hooks to perform pre-processings and post-processings.

The principle for ordering calls is to follows the order of appearance. As such, inside a stage, the jobs will be called
following the same order than how they appear in the application. Same for the order of calling 'before all' hooks,
'before each' hooks, 'after each' hooks, and 'after all' hooks.

PIRUPY was inspired by :

* gitlab-ci pipelines for the model ;
* JUnit for the annotation-based system ;
* and my distaste for yaml.

# How to use

## Logging

PIRUPY use a logger named 'pipeline_runner'

## Requirements on annotaded functions

Jobs and hooks functions are provided with a keyword argument `env`, a dictionnary containing resources to
be used to perform the job and the hooks.

The `env` dictionnary is returned by the pipeline function. The pipeline function usually create the
dictionnary, whereas hooks functions add ('before all' and 'before each' hooks) or remove ('after all' and 'after each'
hooks) ressources into the dictionnary.

Each jobs execution (that includes the hooks 'before_each' and 'after_each') are provided with a clone of this environment, meaning that a jobs cannot interfere (adding or substracting keys) with the environment content of the next jobs. Of course, any mutable object in the environment can be changed by a job for the next.

## Typical use

```python
    #... skipping imports, logging config, etc...

    @pipeline(stages=("first_stage","second_stage","third_stage"))
    def performMySuiteOfTests(env:dict = {}):
        logging.info("Start of pipeline -- init")
        logging.debug(env)
        return env

    @job(stage="first_stage")
    def B(*, env:dict = {}):
        logging.info("performing... B")
        pass

    @job(stage="first_stage")
    def A(*, env:dict = {}):
        logging.info("performing... A")
        pass

    @job(stage="second_stage")
    def C(*, env:dict = {}):
        logging.info("performing... C")
        pass

    @job(stage="second_stage")
    def F(*, env:dict = {}):
        logging.info("performing... F")
        pass

    @job(stage="third_stage")
    def E(*, env:dict = {}):
        logging.info("performing... E")
        pass

    @job(stage="second_stage")
    def D(*, env:dict = {}):
        logging.info("performing... D")
        pass

    @job(stage="third_stage")
    def G(*, env:dict = {}):
        logging.info("performing... G")
        pass

    @job()
    def H(*, env:dict = {}): # performed at each stage
        logging.info("performing... H")
        pass

    @before_all
    def setup(*, env:dict = {}):
        logging.info("performing... setup")
        pass

    @after_all
    def teardown(*, env:dict = {}):
        logging.info("performing... teardown")
        pass

    @before_each(stage="first_stage")
    def enter_first_stage_job(*, env:dict = {}): # called only before performing each job of a given stage
        logging.info("performing... enter_first_stage_job")
        pass

    @after_each
    def exit_job(*, env:dict = {}): # called after each jobs has been called during any stage.
        logging.info("performing... exit_job")
        pass

    ### Ready to run
    if __name__ == "__main__":
        logging.warn("before pipeline")
        performMySuiteOfTests(env={'dir.current':'this/path', 'dir.basedir':'that/path'})
        logging.warn("after pipeline")
```

---
(c) 2022 David SPORN

---
PIRUPY is free software: you can redistribute it and/or modify it under the terms of
the GNU General Public License as published by the Free Software Foundation, either
version 3 of the License, or (at your option) any later version.

PIRUPY is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with PIRUPY.
If not, see <https://www.gnu.org/licenses/>. 

---
