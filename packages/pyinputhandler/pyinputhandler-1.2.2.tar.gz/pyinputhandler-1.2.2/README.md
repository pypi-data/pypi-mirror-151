<!-- Shields -->
[![Contributors][contributors-shield]][contributors-url]
[![Stars][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Repo Size][repo-size-shield]][repo-size-url]
[![MIT License][license-shield]][license-url]

<h1 align="center">InputHandler</h1>
<h3 align="center">A (basic) cross-platform python input handler</h3>

<!-- Table of Contents -->
<details open="open">
    <summary>Table of Contents</summary>
    <ol>
        <li>
            <a href="#about-the-project">About The Project</a>
        </li>
        <li>
            <a href="#getting-started">Getting Started</a>
            <ul>
                <li><a href="#installation">Installation</a></li>
            </ul>
        </li>
        <li>
            <a href="#usage">Usage</a>
        </li>
        <li>
            <a href="#license">License</a>
        </li>
        <li>
            <a href="#acknowledgements">Acknowledgements</a>
        </li>
    </ol>
</details>

<!-- About the Project -->
## About The Project

This project aims to implement a finer control for the input, especially when in use with threads.

It was partially inspired by aiming to be a cross-platform alternative to the `get_line_buffer` 
function from the Unix only python standard library `readline`.

<!-- Getting Started -->
## Getting Started

For the manual installation you must have `setuptools` installed.

Python usually comes with `setuptools`, but if yours does not, then run
  ```sh
  pip install --upgrade setuptools
  ```

Then clone the repository
  ```sh
  git clone https://github.com/DaHunterTime/InputHandler
  ```

And move to the newly cloned folder
  ```sh
  cd InputHandler
  ```

### Installation

Manual installation:

For a manual installation you can use any of the following options.

1. Using python (not recommended)
    * Run the following line in your terminal
      ```sh
      python setup.py install
      ```
    * To uninstall you must remove the files manually
2. Using pip
    * Run the following line in your terminal
      ```sh
      pip install .
      ```
    * To uninstall run
      ```sh
      pip uninstall pyinputhandler
      ```

Pip installation:

* To install run
  ```sh
  pip install pyinputhandler
  ```
* To uninstall run
  ```sh
  pip uninstall pyinputhandler
  ```

<!-- Usage Examples -->
## Usage

To begin with, we can import the library with
  ```python
  import inputhandler
  ```

Or you can import specific things like `buffer_input`
  ```python
  from inputhandler import buffer_input
  ```

We can use the `try_input` like
  ```python
  from inputhandler import try_input

  n = try_input("Enter an integer: ", cast=int, default=0)
  ```

The previous code will prompt the user for an integer, process the input and then turn it into an 
`int` if it can, otherwise it returns the specified default value.

For more uses and tests you can execute the specific test file from `tests` or run `python test.py` 
to select which test to run.

<!-- License -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- Acknowledgements -->
## Acknowledgements

None of the following are associated with the project in any way. They are mentioned as a source of 
learning and inspiration for parts of this project.

* [README Template](https://github.com/othneildrew/Best-README-Template)
* [Cross-Platform getch() for Python](https://gist.github.com/jfktrey/8928865)
* [Windows Cursor Position](https://github.com/tartley/colorama/blob/master/colorama/win32.py)

<!-- Links -->
[contributors-shield]: https://img.shields.io/github/contributors/DaHunterTime/InputHandler.svg?style=for-the-badge
[contributors-url]: https://github.com/DaHunterTime/InputHandler/graphs/contributors
[stars-shield]: https://img.shields.io/github/stars/DaHunterTime/InputHandler.svg?style=for-the-badge
[stars-url]: https://github.com/DaHunterTime/InputHandler/stargazers
[issues-shield]: https://img.shields.io/github/issues/DaHunterTime/InputHandler.svg?style=for-the-badge
[issues-url]: https://github.com/DaHunterTime/InputHandler/issues
[repo-size-shield]: https://img.shields.io/github/repo-size/DaHunterTime/InputHandler.svg?style=for-the-badge
[repo-size-url]: https://github.com/DaHunterTime/InputHandler/archive/refs/heads/main.zip
[license-shield]: https://img.shields.io/github/license/DaHunterTime/InputHandler.svg?style=for-the-badge
[license-url]: https://github.com/DaHunterTime/InputHandler/blob/main/LICENSE
