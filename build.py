from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")


name = "aws_cfn_custom_resource_handler"
default_task = "publish"

@init
def initialize(project):

    project.build_depends_on("mock")
    project.build_depends_on("unittest2")
    project.depends_on("yapsy")
    project.depends_on("boto")
    project.depends_on("requests")
    project.depends_on("json")
