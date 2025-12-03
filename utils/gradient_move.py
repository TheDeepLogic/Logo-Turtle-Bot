from __future__ import print_function
import time
import matplotlib.pyplot as plt


def sgn(x):
    return x / abs(x)


def move_diagonal(_from, _to, delta=10, debug=False, sleep=True, plot=True):
    start_at = complex(*_from)
    destination = complex(*_to)

    position = start_at
    gradient = destination - position
    num_steps = int(round(abs(gradient.real) / delta))

    if debug:
        print('Number of steps: ', num_steps)
        if plot:
            plt.ion()
            plt.plot([position.real, destination.real], [position.imag, destination.imag])

    for i in range(num_steps):
        x_diff = delta * sgn(gradient.real)

        # TODO move x here by x_diff
        if sleep:
            time.sleep(0.2)

        position += x_diff

        real_y_val = start_at.imag + i * delta * sgn(gradient.real) * gradient.imag / gradient.real

        while abs(position.imag - real_y_val) >= delta/2.:
            if debug:
                print('updating y: {}, real: {}'.format(position, real_y_val), end=', ')
                # print(sgn(gradient.imag))
                # print(position.imag, real_y_val)

            y_diff = delta * sgn(gradient.imag)
            position += y_diff * 1j

            if debug and plot:
                    plt.scatter(position.real, position.imag)

            # TODO move y here by y_diff

            if sleep:
                time.sleep(0.2)


if __name__ == '__main__':
    move_diagonal([1000, 1000], [100, 100], delta=40, plot=True, debug=True, sleep=True)
