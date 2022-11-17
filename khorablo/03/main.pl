#!/usr/bin/env perl

my %colors = (
    'lightsalmon' => {'R' => 255, 'G' => 160, 'B' => 122},
    'salmon' => {'R' => 250, 'G' => 128, 'B' => 114},
    'darksalmon' => {'R' => 233, 'G' => 150, 'B' => 122},
    'lightcoral' => {'R' => 240, 'G' => 128, 'B' => 128},
    'indianred' => {'R' => 205, 'G' => 92, 'B' => 92},
    'red' => {'R' => 255, 'G' => 0, 'B' => 0}
);


sub detect_color
{
    my @answer = (undef, 442);
    my %input = @_;
    foreach (keys %colors) {
        $x = sqrt(($colors{$_}{'R'} - $input{'R'})**2 +
            ($colors{$_}{'G'} - $input{'G'})**2 +
            ($colors{$_}{'B'} - $input{'B'})**2);

        if ($x == $answer[1]) {
            @answer = (undef, undef);
            break;
        }

        if ($x < $answer[1]) {
            @answer = ($_, $x);
        }
    }

    return $answer[0];
}


print "R G B: ";
my ($r, $g, $b) = split /\s */, <>;
$output = detect_color(('R' => int($r), 'G' => int($g), 'B' => int($b)));
print "$output\n";
