Feature: ptolemy accurately compiles source files
As a ptolemy user
I want ptolemy to accurately compile my source files
So I don't have to write lengthy table mappings

Scenario: user compiles source files
  When I run ptolemy against some source files
  Then the generated mappings match the expected mappings
