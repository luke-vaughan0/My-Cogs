from .vote import vote


def setup(bot):
    bot.add_cog(vote(bot))

