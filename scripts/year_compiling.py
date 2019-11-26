from argparse import ArgumentParser

from congress_voting.data_loading import save_data

parser = ArgumentParser()
parser.add_argument('--start', help='the year you want to start compiling and saving', type=int, required=True)
parser.add_argument('--end', help='the year you want to stop compiling and saving', type=int, required=True)
parser.add_argument('--data_loc', help="the location of the 'raw_data' folder with saved votes",
                    type=str, required=False, default='data/')
parser.add_argument('--out', help='the location where you want to store the compiled data',
                    type=str, required=False, default='data/')
args = parser.parse_args()
save_data(args.start, args.end, args.data_loc, args.out)
